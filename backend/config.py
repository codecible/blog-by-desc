"""
配置管理模块

使用单例模式管理应用程序配置。
"""

import os
from dataclasses import dataclass
import logging
from typing import Optional
from backend.utils.string import parse_bool

logger = logging.getLogger(__name__)

@dataclass
class Config:
    """配置类

    用于管理应用程序的所有配置项。配置值优先从环境变量中读取，
    如果环境变量不存在，则使用默认值。
    使用单例模式确保全局只有一个配置实例。
    """

    _instance: Optional['Config'] = None
    _initialized: bool = False

    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 确保只初始化一次
        if self._initialized:
            return

        self._initialized = True

        # AI提供商配置
        self.AI_PROVIDER = os.getenv("AI_PROVIDER", "monica")  # 默认使用monica
        logger.info(f"加载配置: AI_PROVIDER={self.AI_PROVIDER}")

        # 验证AI提供商
        if self.AI_PROVIDER not in ["monica", "zhipu"]:
            logger.error(f"不支持的AI提供商: {self.AI_PROVIDER}")
            raise ValueError(f"不支持的AI提供商: {self.AI_PROVIDER}")

        # Monica AI配置
        self.MONICA_API_ENDPOINT = os.getenv("MONICA_API_ENDPOINT", "https://openapi.monica.im/v1")
        self.MONICA_API_KEY = os.getenv("MONICA_API_KEY")
        self.MONICA_MODEL = os.getenv("MONICA_MODEL", "gpt-4o-mini")

        # 智谱AI配置
        self.ZHIPU_API_ENDPOINT = os.getenv("ZHIPU_API_ENDPOINT", "https://open.bigmodel.cn/api/paas/v4")
        self.ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
        self.ZHIPU_MODEL = os.getenv("ZHIPU_MODEL", "glm-4")

        # 记录当前使用的模型
        if self.AI_PROVIDER == "monica":
            logger.info(f"使用Monica AI模型: {self.MONICA_MODEL}")
        else:
            logger.info(f"使用智谱AI模型: {self.ZHIPU_MODEL}")

        # 通用AI配置
        self.API_TEMPERATURE = float(os.getenv("API_TEMPERATURE", "0.7"))
        self.API_MAX_TOKENS = int(os.getenv("API_MAX_TOKENS", "5000"))
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", "1"))
        self.RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))

        # 文章配置
        self.MIN_WORD_COUNT = int(os.getenv("MIN_WORD_COUNT", "1000"))
        self.MAX_WORD_COUNT = int(os.getenv("MAX_WORD_COUNT", "3000"))
        self.MIN_CORE_WORD_COUNT = int(os.getenv("MIN_CORE_WORD_COUNT", "300"))

        # 缓存配置
        self.CACHE_ENABLED = parse_bool(os.getenv("CACHE_ENABLED", "false"))
        self.CACHE_EXPIRE_TIME = int(os.getenv("CACHE_EXPIRE_TIME", "3600"))

        logger.info(f"config: cache_enabled: {self.CACHE_ENABLED}")

        # 验证必需的配置项
        self._validate_config()

    def _validate_config(self):
        """验证关键配置项是否存在"""
        if self.AI_PROVIDER == "monica" and not self.MONICA_API_KEY:
            raise ValueError("使用Monica AI时必须设置MONICA_API_KEY环境变量")
        elif self.AI_PROVIDER == "zhipu" and not self.ZHIPU_API_KEY:
            raise ValueError("使用智谱AI时必须设置ZHIPU_API_KEY环境变量")

    @classmethod
    def get_instance(cls) -> 'Config':
        """
        获取配置实例

        Returns:
            Config: 配置实例
        """
        return cls()
