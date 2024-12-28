"""
路径管理模块

提供项目中所需的各种路径常量和工具函数。
"""

import os
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# 日志相关路径
LOG_DIR = os.path.join(ROOT_DIR, 'logs', 'app')

# 输出文件路径
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')

# 缓存路径
CACHE_DIR = os.path.join(ROOT_DIR, 'cache')

def ensure_dir(dir_path: str) -> None:
    """
    确保目录存在，如果不存在则创建

    Args:
        dir_path: 目录路径
    """
    os.makedirs(dir_path, exist_ok=True)

# 确保必要的目录存在
ensure_dir(LOG_DIR)
ensure_dir(OUTPUT_DIR)
ensure_dir(CACHE_DIR)
