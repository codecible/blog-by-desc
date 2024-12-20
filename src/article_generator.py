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

    async def _call_api_with_retry(self, messages: List[Dict[str, str]]) -> str:
        """带重试机制的API调用
        
        Args:
            messages: 消息列表，包含 role 和 content
            
        Returns:
            str: API 响应的文本内容
        """
        for attempt in range(config.MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=config.API_MODEL or "gpt-4o-mini",
                    messages=messages,
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

        messages = [
            {
                "role": "system",
                "content": "你是一位资深的内容策划专家，擅长选题规划、热点分析和受众洞察，能够精准提炼写作方向。请根据用户提供的描述内容和核心方向，生成相关的写作建议。"
            },
            {
                "role": "user",
                "content": f"描述内容：{description}\n{f'核心主题是：{core_idea}' if core_idea else ''}\n\n"
                          "请根据以上信息提炼3-5个潜在写作方向，这些方向应当：\n\n"
                          "1. 紧密结合描述内容，体现其核心价值\n"
                          "2. 考虑当前社会热点与读者兴趣\n" 
                          "3. 至少一个方向需与核心方向高度相关（如提供）\n\n"
                        "直接输出关键词,无需其他说明文字\n"
                        "请按照以下格式输出:\n"
                        "方向1，方向2，方向3，方向4，方向5"
                 }
        ]
        
        logging.info(f"正在生成写作方向，描述：{description}, 核心主题：{core_idea}")
        response = await self._call_api_with_retry(messages)
        directions = [d.strip().lstrip('1234567890. ') for d in response.split('，')]
        
        self._set_cached_result(cache_key, ','.join(directions))
        logging.info(f"生成的写作方向：{directions}")
        return directions

    async def generate_title(self, directions: List[str]) -> str:
        """异步生成标题"""
        cache_key = f"title:{','.join(directions)}"
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result

        messages = [
            {
                "role": "system",
                "content": (
                    "你是一位资深的自媒体内容策划专家，具有以下专业能力：\n"
                    "1. 深谙各大内容平台的标题特点和算法偏好\n"
                    "2. 精通不同受众群体的心理需求和阅读习惯\n" 
                    "3. 擅长运用多种标题写作技巧和创意方法\n"
                    "4. 具备数据分析能力，了解各类标题的转化效果\n"
                    "5. 熟悉热点事件和行业动态，能够及时抓住时事热点"
                )
            },
            {
                "role": "user", 
                "content": (
                    f"基于以下写作方向生成3个不同风格的标题：\n{', '.join(directions)}\n\n"
                    "1. 标题长度控制在10-25字之间\n"
                    "2. 包含数字/具体数据更佳\n"
                    "3. 使用吸引眼球的关键词（如：秘密、揭秘、独家、终极等）\n"
                    "4. 适当使用标点符号增加感染力\n"
                    "5. 确保标题真实可信，避免过度夸张\n\n"
                    "请直接输出标题，无需其他说明文字"
                )
            }
        ]
        
        logging.info(f"正在生成标题，写作方向：{directions}")
        title = await self._call_api_with_retry(messages)
        
        self._set_cached_result(cache_key, title)
        logging.info(f"生成的标题：{title}")
        return title

    async def generate_content(self, directions: List[str], title: str) -> str:
        """异步生成文章内容"""
        cache_key = f"content:{title}:{','.join(directions)}"
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result



        messages = [
            {
                "role": "system",
                "content": (
                    f"你是一名经验丰富的自媒体创作者，擅长将复杂信息转化为生动、易读且风格鲜明的文章。"
                    f"根据以下用户提供的信息，创作一篇{config.MIN_WORD_COUNT}-{config.MAX_WORD_COUNT}字的内容，"
                    "目标是吸引读者的兴趣，保持内容条理清晰并充满吸引力。请特别注重以下几点：\n\n"
                    "1. 明确主题：以用户的核心信息为中心展开，保持文章主题鲜明。\n"
                    "2. 易读性：使用通俗易懂的语言，避免过多专业术语。\n"
                    "3. 生动表达：通过故事化叙述、类比和有趣的例子使文章更具吸引力。\n"
                    "4. 逻辑结构：确保文章条理清晰，层层递进，逻辑紧密。\n"
                    "5. 适当数据支持：根据需要加入相关统计、案例或趋势数据来增强说服力。\n"
                    "6. 风格独特：结合轻松幽默、专业权威或亲切感的写作风格，吸引目标读者群体。"
                )
            },
            {
                "role": "user",
                "content": (
                    "请根据以下信息撰写文章：\n"
                    f"标题：{title}\n"
                    f"写作方向：{', '.join(directions)}"
                )
            }
        ]
        
        logging.info(f"正在生成文章内容，标题：{title}")
        content = await self._call_api_with_retry(messages)
        
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
{'\n'.join(directions)}

## 正文
{content}
"""
        
        # 保存文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        logging.info(f"文章已保存到：{filename}")
        return filename 