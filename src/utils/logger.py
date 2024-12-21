import os
import logging
from datetime import datetime
from ..config import Config

def setup_logging():
    """设置日志配置"""
    os.makedirs('logs', exist_ok=True)
    config = Config()
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format=config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(
                f'logs/{datetime.now().strftime("%Y%m%d")}.log', 
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__) 