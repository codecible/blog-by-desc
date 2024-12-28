import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from utils.paths import LOG_DIR

def setup_logging() -> logging.Logger:
    """
    设置日志配置

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 获取根日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 清除现有的处理器
    logger.handlers.clear()

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # 创建文件处理器
    today = datetime.now().strftime('%Y%m%d')
    file_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, f'{today}.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(name)s:%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    return logger
