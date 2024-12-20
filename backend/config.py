from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Config:
    """配置类"""
    
    # API配置
    API_ENDPOINT = "https://openapi.monica.im/v1"    # Monica API的基础URL
    AI_MODEL = "gpt-4o-mini"                  # 使用的AI模型
    API_TEMPERATURE = 0.7                      # 控制输出的随机性 (0.0-1.0)
    API_MAX_TOKENS = 2000                      # 限制输出的最大长度
    MAX_RETRIES = 1                           # 最大重试次数
    RETRY_DELAY = 2                           # 重试延迟时间（秒）
    
    # 缓存配置
    CACHE_ENABLED = True                      # 是否启用缓存
    CACHE_EXPIRE_TIME = 3600                  # 缓存过期时间（秒）
    
    # 日志配置
    LOG_LEVEL = "INFO"                        # 日志级别
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s:%(funcName)s:%(lineno)d] %(message)s"
    
    # 文章配置
    MIN_WORD_COUNT = 500                      # 文章最小字数
    MAX_WORD_COUNT = 1000                     # 文章最大字数
