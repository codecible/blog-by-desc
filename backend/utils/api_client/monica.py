"""
Monica AI API客户端实现

这个模块提供了Monica AI API的具体实现。
"""

import logging
from typing import Dict, List, Optional, Union
from openai import AsyncOpenAI

from ...config import Config
from .base import BaseAPIClient, Message

logger = logging.getLogger(__name__)

class MonicaAPIClient(BaseAPIClient):
    """Monica AI API客户端实现类"""
    
    def __init__(self):
        """
        初始化Monica AI客户端
        
        从配置中获取API密钥和端点信息
        """
        self.config = Config()
        
        # 确保使用Monica AI
        if self.config.AI_PROVIDER != "monica":
            raise ValueError("配置的AI提供商不是Monica")
            
        # 初始化异步OpenAI客户端
        self.client = AsyncOpenAI(
            base_url=self.config.MONICA_API_ENDPOINT,
            api_key=self.config.MONICA_API_KEY
        )
        
    async def call_api(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        **kwargs
    ) -> str:
        """
        调用Monica AI API
        
        Args:
            prompt: 简单模式下的提示词
            messages: 高级模式下的消息列表
            **kwargs: 其他参数，如temperature、max_tokens等
            
        Returns:
            str: AI生成的响应文本
            
        Raises:
            ValueError: 当参数无效时
            Exception: 当API调用失败时
        """
        try:
            # 如果没有提供messages，则使用prompt创建默认消息
            if messages is None:
                if prompt is None:
                    raise ValueError("必须提供prompt或messages参数")
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            
            # 创建完成请求
            completion = await self.client.chat.completions.create(
                model=self.config.MONICA_MODEL,
                messages=messages,
                temperature=kwargs.get('temperature', self.config.API_TEMPERATURE),
                max_tokens=kwargs.get('max_tokens', self.config.API_MAX_TOKENS)
            )
            
            # 返回生成的文本内容
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Monica API调用出错: {str(e)}")
            raise 