"""
API客户端工厂模块

这个模块负责创建不同AI提供商的API客户端实例。
"""

import logging
from typing import Dict, Type

from .base import BaseAPIClient
from .monica import MonicaAPIClient
from .zhipu import ZhipuAPIClient

logger = logging.getLogger(__name__)

class APIClientFactory:
    """API客户端工厂类"""
    
    # 注册可用的AI提供商
    _clients: Dict[str, Type[BaseAPIClient]] = {
        "monica": MonicaAPIClient,
        "zhipu": ZhipuAPIClient
    }
    
    @classmethod
    def create_client(cls, model_type: str) -> BaseAPIClient:
        """
        创建API客户端实例
        
        Args:
            model_type: AI提供商类型，如"monica"或"zhipu"
            
        Returns:
            BaseAPIClient: API客户端实例
            
        Raises:
            ValueError: 当提供的model_type不支持时
        """
        try:
            if model_type not in cls._clients:
                raise ValueError(f"不支持的模型类型: {model_type}")
                
            client_class = cls._clients[model_type]
            return client_class()
            
        except Exception as e:
            logger.error(f"创建API客户端失败: {str(e)}")
            raise 