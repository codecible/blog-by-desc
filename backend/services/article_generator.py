"""
文章生成器模块

这个模块负责文章的生成、缓存和存储。
"""

import os
import logging
import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime

from backend.utils.api_client import APIClient
from backend.utils.cache import Cache
from backend.config import Config
from backend.schemas.article import ArticleRequest, ArticleResponse, ArticleData

logger = logging.getLogger(__name__)

class ArticleGenerator:
    """
    文章生成器：负责文章的生成、缓存和存储

    主要功能：
    1. 根据描述和核心主题生成文章内容
    2. 将生成的文章保存到文件

    属性：
        api_client: API客户端，用于调用AI接口
        cache: 缓存客户端，用于缓存生成结果
        config: 配置对象，包含文章生成的相关配置
    """

    def __init__(self, model_type: Optional[str] = None):
        """
        初始化文章生成器

        Args:
            model_type: AI提供商类型，如果不指定则使用配置文件中的设置
        """
        # 如果未指定model_type，从配置中获取
        if model_type is None:
            config = Config.get_instance()
            model_type = config.AI_PROVIDER

        self.api_client = APIClient(model_type)
        self.cache = Cache()
        self.config = Config.get_instance()

    def _get_cache_key(self, *args) -> str:
        """
        生成缓存键

        Args:
            *args: 用于生成缓存键的参数列表

        Returns:
            str: MD5格式的缓存键
        """
        # 获取模型信息
        provider = self.api_client.client.config.AI_PROVIDER
        model = (
            self.api_client.client.config.MONICA_MODEL
            if provider == "monica"
            else self.api_client.client.config.ZHIPU_MODEL
        )
        # 添加提供商和模型信息到缓存键
        content = f"{provider}:{model}:" + ''.join(str(arg) for arg in args)
        return hashlib.md5(content.encode()).hexdigest()

    async def generate_content(
        self,
        description: str,
        core_idea: Optional[str] = None
    ) -> str:
        """
        生成文章内容

        Args:
            description: 文章描述
            core_idea: 核心观点（可选）

        Returns:
            str: 生成的文章内容

        Raises:
            Exception: 当API调用失败时抛出
        """
        try:
            cache_key = self._get_cache_key('content', description, core_idea)
            cached_result = self.cache.get(cache_key)
            if cached_result:
                logger.info("使用缓存的文章内容")
                return cached_result

            min_word_count = self.config.MIN_WORD_COUNT * 3
            max_word_count = self.config.MAX_WORD_COUNT * 3
            min_core_word_count = self.config.MIN_CORE_WORD_COUNT * 3

            messages = [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"你是一位经验丰富的微信公众号爆文创作者，拥有丰富的写作技巧和对热点传播的敏感度。请基于下面提供的信息，创作一篇{min_word_count} - {max_word_count}字的文章，并以markdown格式输出。\n\n"
                                "【创作要求】\n\n"
                                "1. 内容要求\n"
                                "- 主题鲜明，观点突出\n"
                                "- 论证充分，案例丰富\n"
                                "- 结构清晰，层次分明\n"
                                "- 语言生动，表达流畅\n"
                                f"- 特别强调，必须要遵循的：每个主题下的数据字数不少于{min_core_word_count}个字 。写完后请注意检查是否符合标准\n"
                                "2. 写作技巧\n"
                                "- 开篇要吸引读者注意\n"
                                "- 善用故事化表达\n"
                                "- 适当运用数据支撑\n"
                                "- 结尾给出思考启发\n\n"
                                "3. 格式规范\n"
                                "- 使用markdown语法\n"
                                "- 标题层级清晰(#、##、###)\n"
                                "- 重点内容加粗(**文字**)\n"
                                "- 适当使用列表和引用\n"
                                "- 段落间留出适当空行\n\n"
                                "请确保文章:\n"
                                "1. 符合专业性要求\n"
                                "2. 内容通俗易懂\n"
                                "3. 观点论证充分\n"
                                "4. 文章流畅自然"
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
                                f"描述：{description}\n"
                                f"核心观点：{core_idea if core_idea else '无'}"
                            )
                        }
                    ]
                }
            ]

            content = await self.api_client.call_api(messages=messages)
            if not content:
                raise ValueError("生成的文章内容为空")

            self.cache.set(cache_key, content)
            logger.info(f"成功生成文章内容，长度: {len(content)}")
            return content

        except Exception as e:
            logger.error(f"生成文章内容时发生错误: {str(e)}")
            raise

    def save_article(
        self,
        content: str
    ) -> str:
        """
        保存文章到文件

        Args:
            content: 文章内容

        Returns:
            str: 保存的文件路径

        Raises:
            OSError: 当文件创建或写入失败时抛出
        """
        try:
            os.makedirs('output', exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            filename = f"output/{timestamp}.md"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"文章已保存到: {filename}")
            return filename

        except OSError as e:
            logger.error(f"保存文章时发生错误: {str(e)}")
            raise

    def switch_model(self, model_type: str) -> None:
        """
        切换AI模型类型

        Args:
            model_type: 新的AI提供商类型
        """
        current_provider = self.api_client.client.config.AI_PROVIDER
        if model_type != current_provider:
            logger.info(f"切换AI提供商: {current_provider} -> {model_type}")
            self.api_client = APIClient(model_type)

    async def generate(self, request: ArticleRequest) -> ArticleResponse:
        """
        生成文章的主要流程

        Args:
            request: 文章生成请求对象

        Returns:
            ArticleResponse: 生成的文章响应对象

        Raises:
            Exception: 当文章生成过程中发生错误时抛出
        """
        logger.info(f"开始生成文章: 描述长度={len(request.description)}, AI提供商={request.model_type}")

        try:
            # 如果需要，切换到新的模型
            self.switch_model(request.model_type)

            # 生成文章内容
            content = await self.generate_content(request.description, request.core_idea)

            # 保存文章
            file_path = self.save_article(content)

            # 创建响应
            response = ArticleResponse(
                success=True,
                message="文章生成成功",
                data=ArticleData(
                    content=content,
                    file_path=file_path
                )
            )

            logger.info(f"文章生成成功: 文件={file_path}, AI提供商={request.model_type}, 内容长度={len(content)}")
            return response

        except Exception as e:
            logger.error(f"生成文章时发生错误: {str(e)}, AI提供商={request.model_type}")
            raise
