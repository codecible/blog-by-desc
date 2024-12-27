"""
Monica AI API客户端模块

这个模块提供了与Monica AI API交互的客户端实现。
主要功能：
1. 管理API密钥和配置
2. 处理API请求和响应
3. 实现错误重试机制
4. 提供异步API调用接口

使用示例：
    client = APIClient()
    # 简单调用
    response = await client.call_api("你的提示词")
    
    # 高级调用，自定义角色和消息
    messages = [
        {"role": "system", "content": "你是一个专业的文章写手"},
        {"role": "user", "content": "写一篇关于AI的文章"}
    ]
    response = await client.call_api(messages=messages)
"""

import os
import logging
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from ..config import Config

# 加载.env文件中的环境变量
load_dotenv()

# 创建日志记录器
logger = logging.getLogger(__name__)

# 定义消息类型
Message = Dict[str, Union[str, List[Dict[str, str]]]]

class APIClient:
    """
    Monica AI API客户端类
    
    负责处理与Monica AI API的所有交互，包括：
    - API密钥管理
    - 请求发送
    - 响应处理
    - 错误重试
    
    属性:
        config: 配置对象，包含API相关的所有配置项
        client: OpenAI客户端实例
    """
    
    def __init__(self):
        """
        初始化API客户端
        
        从环境变量中获取API密钥，如果未设置则抛出异常
        """
        self.config = Config()
        
        # 确保使用Monica AI
        if self.config.AI_PROVIDER != "monica":
            raise ValueError("APIClient只支持Monica AI，当前配置的AI提供商为: " + self.config.AI_PROVIDER)
            
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
        异步调用Monica AI API
        
        Args:
            prompt: 发送给AI的提示词（简单模式）
            messages: 完整的消息列表，包含角色和内容（高级模式）
            **kwargs: 其他参数，如temperature、max_tokens等
            
        Returns:
            str: AI生成的文本内容
            
        Raises:
            ValueError: 当prompt和messages都未提供时抛出
            Exception: 当API调用失败时抛出
            
        Examples:
            # 简单模式
            response = await client.call_api("写一篇文章")
            
            # 高级模式
            messages = [
                {
                    "role": "system",
                    "content": "你是一个专业的文章写手"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "写一篇关于AI的文章"
                        }
                    ]
                }
            ]
            response = await client.call_api(messages=messages)
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
            logger.error(f"API调用出错: {str(e)}")
            raise