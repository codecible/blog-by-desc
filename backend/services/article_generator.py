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

            min_word_count = self.config.MIN_WORD_COUNT
            max_word_count = self.config.MAX_WORD_COUNT
            min_core_word_count = self.config.MIN_CORE_WORD_COUNT

            messages = [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"你是一位经验丰富的微信公众号爆文创作者，拥有丰富的写作技巧和对热点传播的敏感度。请基于下面提供的信息，创作一篇{min_word_count} - {max_word_count}字的文章，并以markdown格式输出。\n\n"
                                f"【创作要求】\n\n"
                                f"1. 内容要求\n"
                                f"- 文章总字数控制在{min_word_count} - {max_word_count}之间\n"
                                "- 主题鲜明，观点突出\n"
                                "- 可以有二级标题，不能有小标题\n"
                                "- 语言生动，表达流畅\n"
                                "- 避免表情符号，请勿使用表情符号\n"
                                f"- 特别强调，必须要遵循的：每个主题下的数据字数不少于{min_core_word_count}个字 。写完后请注意检查是否符合标准\n"
                                "2. 写作技巧\n"
                                "**标题**：吸引人，能够引发读者点击，不超过20个字。\n"
                                "**开头**： 开头要吸引读者注意，不超过100个字。\n"
                                "**内容（一定要遵守，会有人工审核的哦）***：\n"
                                "- **自然融入**：数据和案例应自然融入文章，避免使用 '数据支撑'、'案例'等突兀词汇。\n"
                                "- **丰富性**：每段文字都要丰富、有理有据，包含具体案例、数据支撑或引用权威观点，但需自然嵌入。\n"
                                "- 使用相关数据或研究结果，提升内容的可信度。\n"
                                "- 通过故事情节或情感表达，引发读者的共鸣。\n"
                                "- 在适当位置设置互动性问题，增加读者的参与感。\n\n"
                                "3. 格式规范\n"
                                "- 使用markdown语法\n"
                                "- 标题层级清晰(#、##、###)\n"
                                "- 重点内容加粗(**文字**)\n"
                                "- 适当使用列表和引用\n"
                                "- 段落间留出适当空行\n\n"
                                "请确保文章符合以上要求，适合微信公众号发布。"
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

    async def generate_titles(self, description: str, platform: str = "xiaohongshu") -> List[str]:
        """
        生成多个标题建议

        Args:
            description: 文章描述
            platform: 目标平台，支持 xiaohongshu/weixin/zhihu 等

        Returns:
            List[str]: 生成的标题列表
        """
        try:
            # 构建消息列表
            if platform.lower() == "xiaohongshu":
                messages = [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "作为一位资深小红书标题优化专家，你的任务是依据提供的内容，创作10个风格迥异的标题。以下是具体要求和指南："
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
                                    f"输入内容：\n\n[{description}]\n\n"
                                    "输出要求：\n"
                                    "1. 标题结构规则：\n"
                                    "- 灵活使用'|'分隔符，但非强制\n"
                                    "- 适用于以下场景：\n"
                                    "  * 时间/进度标记：如'DAY15|破PB了'\n"
                                    "  * 场景切换：如'都市|清晨五点的跑步日记'\n"
                                    "  * 身份标记：如'新手记录|第一次5K'\n"
                                    "  * 情绪转换：如'治愈|雨天跑步'\n"
                                    "  * 数据分享：如'配速5:30|半马完赛故事'\n\n"
                                    "2. 风格参考（需涵盖以下几种风格）：\n"
                                    "- 励志激励型：如'100天跑步计划第30天，终于突破了'\n"
                                    "- 专业干货型：如'跑步心率到底该怎么控制？过来人经验分享'\n"
                                    "- 情感共鸣型：如'当代打工人的跑步日记，治愈孤独的良药'\n"
                                    "- 话题互动型：如'你们跑步时都在想些什么？来聊聊'\n"
                                    "- 实用建议型：如'入门级跑鞋推荐，这些百元好物真的香'\n\n"
                                    "3. 具体要求：\n"
                                    "- 每个标题添加2-3个相关emoji\n"
                                    "- 标题长度控制在15-30字之间\n"
                                    "- 根据内容自然选择是否使用分隔符\n"
                                    "- 确保标题具有吸引力和传播潜力\n"
                                    "- 避免标题党和过度营销\n\n"
                                    "附加说明（针对每个标题）：\n"
                                    "- 标题类型：如励志型、干货型等\n"
                                    "- 适用场景：如个人日记、经验分享等\n"
                                    "- 预期效果：如激励、教育、共鸣等\n"
                                )
                            }
                        ]
                    }
                ]
            else:
                raise ValueError(f"不支持的平台类型: {platform}")

            # 调用API生成标题
            content = await self.api_client.call_api(
                messages=messages,
                temperature=0.8,  # 使用较高的温度以获得更多样化的结果
                max_tokens=4095
            )

            # 如果内容为空，抛出异常
            if not content:
                raise ValueError("未能生成有效的标题")

            # 直接返回API生成的内容
            return [content]

        except Exception as e:
            logger.error(f"生成标题失败: {str(e)}")
            raise
