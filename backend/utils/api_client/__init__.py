"""
API客户端包

这个包提供了与不同AI提供商交互的客户端实现。
"""

from typing import Dict, List, Optional, Union
from .base import BaseAPIClient, Message
from .factory import APIClientFactory

class APIClient:
    """
    API客户端类
    
    这个类是所有AI API调用的统一入口。
    它使用工厂模式来创建具体的AI提供商客户端。
    """
    
    def __init__(self, model_type: str = "monica"):
        """
        初始化API客户端
        
        Args:
            model_type: AI提供商类型，默认为"monica"
        """
        self.client = APIClientFactory.create_client(model_type)
        
    async def call_api(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        **kwargs
    ) -> str:
        """
        调用AI API
        
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
        return await self.client.call_api(prompt, messages, **kwargs)

__all__ = [
    'BaseAPIClient',
    'Message',
    'APIClientFactory',
    'APIClient'
] 