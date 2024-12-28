"""
智谱AI API客户端实现

这个模块提供了智谱AI API的具体实现。
参考文档：https://bigmodel.cn/dev/api/normal-model/glm-4
"""

import logging
from typing import Dict, List, Optional, Union
import zhipuai
import json

from backend.config import Config
from backend.utils.api_client.base import BaseAPIClient, Message

logger = logging.getLogger(__name__)

class ZhipuAPIClient(BaseAPIClient):
    """智谱AI API客户端实现类"""

    def __init__(self):
        """
        初始化智谱AI客户端

        从配置中获取API密钥和端点信息
        """
        self.config = Config.get_instance()

        # 初始化智谱AI客户端
        zhipuai.api_key = self.config.ZHIPU_API_KEY
        self.client = zhipuai.ZhipuAI(api_key=self.config.ZHIPU_API_KEY)
        logger.info(f"初始化智谱AI客户端成功，使用模型: {self.config.ZHIPU_MODEL}")

    def _convert_message(self, message: Message) -> Dict:
        """
        转换消息格式以适配智谱AI的API

        Args:
            message: 原始消息

        Returns:
            Dict: 转换后的消息
        """
        if isinstance(message.get('content'), list):
            # 如果content是列表（Monica格式），提取文本内容
            content_list = message['content']
            text_parts = []
            for item in content_list:
                if isinstance(item, dict) and item.get('type') == 'text':
                    text_parts.append(item['text'])
            content = ' '.join(text_parts)
        else:
            content = message.get('content', '')

        return {
            "role": message.get('role', 'user'),
            "content": content
        }

    async def call_api(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        **kwargs
    ) -> str:
        """
        调用智谱AI API

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
                        "content": prompt
                    }
                ]

            # 转换消息格式
            logger.info(f"原始消息列表: {json.dumps(messages, ensure_ascii=False, indent=2)}")
            converted_messages = [self._convert_message(msg) for msg in messages]
            logger.info(f"转换后的消息列表: {json.dumps(converted_messages, ensure_ascii=False, indent=2)}")

            # 创建完成请求
            response = self.client.chat.completions.create(
                model=self.config.ZHIPU_MODEL,
                messages=converted_messages,
                temperature=kwargs.get('temperature', self.config.API_TEMPERATURE),
                # 用温度取样的另一种方法，称为核取样 取值范围是： [0.0,1.0]
                # 较小的 top_p：生成更保守、确定性强的文本
                top_p=kwargs.get('top_p', 0.7),
                max_tokens=kwargs.get('max_tokens', 3000),
                stream=False  # 非流式返回
            )

            # 获取生成的内容
            content = response.choices[0].message.content
            logger.info(f"智谱AI API调用成功: 生成内容长度={len(content)}")
            return content

        except Exception as e:
            logger.error(f"智谱AI API调用出错: {str(e)}")
            raise
