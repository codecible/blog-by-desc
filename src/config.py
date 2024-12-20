from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Config:
    # API配置
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2
    
    # 缓存配置
    CACHE_ENABLED: bool = True
    CACHE_EXPIRE_TIME: int = 3600  # 1小时
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] [%(lineno)d] %(message)s"
    
    # 文章生成配置
    MIN_WORD_COUNT: int = 500
    MAX_WORD_COUNT: int = 1000 
    
    # API 调用配置
    API_TEMPERATURE: float = 0.7
    API_MAX_TOKENS: int = 2000
    API_ENDPOINT: str = "https://api.monica.im/v1/chat/completions"