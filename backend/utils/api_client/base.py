"""
基础API客户端抽象类

这个模块定义了所有AI提供商客户端必须实现的接口。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

# 定义消息类型
Message = Dict[str, Union[str, List[Dict[str, str]]]]

class BaseAPIClient(ABC):
    """
    API客户端基类
    
    所有AI提供商的客户端都必须继承这个类并实现其方法。
    """
    
    @abstractmethod
    async def call_api(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        **kwargs
    ) -> str:
        """
        调用AI API的抽象方法
        
        Args:
            prompt: 简单模式下的提示词
            messages: 高级模式下的消息列表
            **kwargs: 其他参数，如temperature、max_tokens等
            
        Returns:
            str: AI生成的响应文本
            
        Raises:
            NotImplementedError: 当子类没有实现此方法时
            Exception: 当API调用失败时
        """
        raise NotImplementedError("子类必须实现call_api方法")