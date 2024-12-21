import os
import logging
import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..utils.api_client import APIClient
from ..utils.cache import Cache
from ..config import Config

logger = logging.getLogger(__name__)

class BlogGenerator:
    """博客文章生成器"""
    
    def __init__(self):
        self.api_client = APIClient()
        self.cache = Cache()
        self.config = Config()
        
    def _get_cache_key(self, *args) -> str:
        """生成缓存键"""
        content = ''.join(str(arg) for arg in args)
        return hashlib.md5(content.encode()).hexdigest()
        
    async def generate_directions(
        self, 
        description: str, 
        core_idea: Optional[str] = None
    ) -> List[str]:
        """生成写作方向"""
        cache_key = self._get_cache_key('directions', description, core_idea)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
            
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一位资深的内容策划专家，擅长选题规划、热点分析和受众洞察，"
                    "能够精准提炼写作方向。请根据用户提供的描述内容和核心方向，"
                    "生成相关的写作建议。"
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            f"描述内容：{description}\n"
                            f"{f'核心主题是：{core_idea}' if core_idea else ''}\n\n"
                            "请根据以上信息提炼3-5个潜在写作方向，这些方向应当：\n\n"
                            "1. 紧密结合描述内容，体现其核心价值\n"
                            "2. 考虑当前社会热点与读者兴趣\n"
                            "3. 至少一个方向需与核心方向高度相关（如提供）\n\n"
                            "直接输出关键词，无需其他说明文字\n"
                            "请按照以下格式输出：\n"
                            "- 方向1\n- 方向2\n- 方向3"
                        )
                    }
                ]
            }
        ]
        
        content = await self.api_client.call_api(messages=messages)
        directions = [line[2:].strip() for line in content.split('\n') if line.startswith('- ')]
        
        self.cache.set(cache_key, directions)
        return directions
        
    async def generate_title(self, directions: List[str]) -> str:
        """生成文章标题"""
        cache_key = self._get_cache_key('title', *directions)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
            
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "你是一位资深的自媒体内容策划专家，具有以下专业能力：\n"
                            "1. 深谙各大内容平台的标题特点和算法偏好\n"
                            "2. 精通不同受众群体的心理需求和阅读习惯\n"
                            "3. 擅长运用多种标题写作技巧和创意方法\n"
                            "4. 具备数据分析能力，了解各类标题的转化效果\n"
                            "5. 熟悉热点事件和行业动态，能够及时抓住��事热点"
                        )
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            f"基于以下写作方向生成3个不同风格的标题：\n"
                            f"{', '.join(directions)}\n\n"
                            "1. 标题长度控制在10-25字之间\n"
                            "2. 包含数字/具体数据更佳\n"
                            "3. 使用吸引眼球的关键词（如：秘密、揭秘、独家、终极等）\n"
                            "4. 适当使用标点符号增加感染力\n"
                            "5. 确保标题真实可信，避免过度夸张\n\n"
                            "请按照以下格式输出：\n"
                            "1. 标题1\n2. 标题2\n3. 标题3"
                        )
                    }
                ]
            }
        ]
        
        content = await self.api_client.call_api(messages=messages)
        titles = [line[3:].strip() for line in content.split('\n') if line.startswith(('1.', '2.', '3.'))]
        title = titles[0] if titles else content
        
        self.cache.set(cache_key, title)
        return title
        
    async def generate_content(
        self, 
        directions: List[str], 
        title: str
    ) -> str:
        """生成文章内容"""
        cache_key = self._get_cache_key('content', title, *directions)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
            
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "你是一名经验丰富的自媒体创作者，擅长将复杂信息转化为生动、易读且风格鲜明的文章。"
                            f"根据以下用户提供的信息，创作一篇{self.config.MIN_WORD_COUNT}-{self.config.MAX_WORD_COUNT}字的内容，"
                            "目标是吸引读者的兴趣，保持内容条理清晰并充满吸引力。请特别注重以下几点：\n\n"
                            "1. 明确主题：以用户的核心信息为中心展开，保持文章主题鲜明\n"
                            "2. 易读性：使用通俗易懂的语言，避免过多专业术语\n"
                            "3. 生动表达：通过故事化叙述、类比和有趣的例子使文章更具吸引力\n"
                            "4. 逻辑结构：确保文章条理清晰，层层递进，逻辑紧密\n"
                            "5. 适当数据支持：根据需要加入相关统计、案例或趋势数据来增强说服力\n"
                            "6. 风格独特：结合轻松幽默、专业权威或亲切感的写作风格，吸引目标读者群体"
                        )
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "请根据以下信息撰写文章：\n"
                            f"标题：{title}\n"
                            f"写作方向：{', '.join(directions)}"
                        )
                    }
                ]
            }
        ]
        
        content = await self.api_client.call_api(messages=messages)
        
        self.cache.set(cache_key, content)
        return content
        
    def save_article(
        self, 
        title: str, 
        content: str, 
        directions: List[str]
    ) -> str:
        """保存文章到文件"""
        os.makedirs('output', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        filename = f"output/{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write("## 写作方向\n\n")
            for direction in directions:
                f.write(f"- {direction}\n")
            f.write("\n## 正文\n\n")
            f.write(content)
            
        return filename