import os
from openai import OpenAI
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from dotenv import load_dotenv
from functools import lru_cache
import time
from .config import Config

# 加载配置
config = Config()

# 加载环境变量
load_dotenv()

# 配置日志
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(f'logs/{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class ArticleGenerator:
    def __init__(self):
        self.api_key = os.getenv('MONICA_API_KEY')
        if not self.api_key:
            raise ValueError("MONICA_API_KEY 环境变量未设置")
            
        # 初始化 OpenAI 客户端，设置 Monica API 基础URL
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=config.API_ENDPOINT  # Monica API 端点
        )
        self._cache: Dict[str, Dict[str, Any]] = {}

    async def _call_api_with_retry(self, prompt: str) -> str:
        """带重试机制的API调用"""
        for attempt in range(config.MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=config.API_TEMPERATURE,
                    max_tokens=config.API_MAX_TOKENS
                )
                return response.choices[0].message.content
            except Exception as e:
                logging.error(f"API调用失败 (尝试 {attempt + 1}/{config.MAX_RETRIES}): {str(e)}")
                if attempt < config.MAX_RETRIES - 1:
                    time.sleep(config.RETRY_DELAY)
                else:
                    raise

    @lru_cache(maxsize=100)
    def _get_cached_result(self, cache_key: str) -> Optional[str]:
        """从缓存获取结果"""
        if not config.CACHE_ENABLED:
            return None
        
        cache_data = self._cache.get(cache_key)
        if cache_data:
            if time.time() - cache_data['timestamp'] < config.CACHE_EXPIRE_TIME:
                return cache_data['result']
            else:
                del self._cache[cache_key]
        return None

    def _set_cached_result(self, cache_key: str, result: str) -> None:
        """设置缓存结果"""
        if config.CACHE_ENABLED:
            self._cache[cache_key] = {
                'result': result,
                'timestamp': time.time()
            }

    async def generate_directions(self, description: str, core_idea: Optional[str] = None) -> List[str]:
        """异步生成写作方向"""
        cache_key = f"directions:{description}:{core_idea}"
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result.split(',')

        prompt = f"请分析以下内容，提供3-5个写作方向，���逗号分隔：\n{description}"
        if core_idea:
            prompt += f"\n核心主题是：{core_idea}"
        
        logging.info(f"正在生成写作方向，描述：{description}, 核心主题：{core_idea}")
        response = await self._call_api_with_retry(prompt)
        directions = [d.strip() for d in response.split(',')]
        
        self._set_cached_result(cache_key, ','.join(directions))
        logging.info(f"生成的写作方向：{directions}")
        return directions

    async def generate_title(self, directions: List[str]) -> str:
        """异步生成标题"""
        cache_key = f"title:{','.join(directions)}"
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result

        prompt = f"基于以下写作方向生成一个吸引人的标题：\n{', '.join(directions)}"
        
        logging.info(f"正在生成标题，写作方向：{directions}")
        title = await self._call_api_with_retry(prompt)
        
        self._set_cached_result(cache_key, title)
        logging.info(f"生成的标题：{title}")
        return title

    async def generate_content(self, directions: List[str], title: str) -> str:
        """异步生成文章内容"""
        cache_key = f"content:{title}:{','.join(directions)}"
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result

        prompt = f"""
        请根据以下写作方向和标题，生成一篇{config.MIN_WORD_COUNT}-{config.MAX_WORD_COUNT}字的文章：
        标题：{title}
        写作方向：{', '.join(directions)}
        要求：
        1. 内容要有逻辑性和连贯性
        2. 分段合理
        3. 语言流畅自然
        """
        
        logging.info(f"正在生成文章内容，标题：{title}")
        content = await self._call_api_with_retry(prompt)
        
        self._set_cached_result(cache_key, content)
        logging.info("文章内容生成完成")
        return content

    def save_article(self, title: str, content: str, directions: List[str]) -> str:
        """保存文章到markdown文件"""
        # 确保output目录存在
        os.makedirs('output', exist_ok=True)
        
        # 生成文件名
        filename = f"output/{datetime.now().strftime('%Y%m%d%H%M')}.md"
        
        # 组织markdown内容
        markdown_content = f"""# {title}

## 写作方向
{', '.join(directions)}

## 正文
{content}
"""
        
        # 保存文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        logging.info(f"文章已保存到：{filename}")
        return filename 