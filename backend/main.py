# 标准库导入
import datetime
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 第三方库导入
import fastapi
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# 本地应用导入
from backend.routers import article
###################
# 初始化配置
###################

# 加载环境变量文件
def load_env_file():
    """加载环境变量文件，按优先级从高到低尝试加载"""
    current_dir = Path(__file__).resolve().parent
    env_files = [
        current_dir / '.env',                    # 本地开发环境
        current_dir / '.env.production',         # 生产环境
        current_dir / '.env.example'             # 示例配置（最低优先级）
    ]

    for env_file in env_files:
        if env_file.exists():
            load_dotenv(env_file)
            print(f"已加载环境变量文件: {env_file}")
            return
    print("警告：未找到任何环境变量文件")

load_env_file()

# 设置 Python 路径
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

###################
# 日志配置
###################

# 确保日志目录存在
log_dir = os.path.join(Path(__file__).resolve().parent, 'logs', 'app')
os.makedirs(log_dir, exist_ok=True)

# 生成日志文件名
log_file = os.path.join(log_dir, f"{datetime.datetime.now().strftime('%Y%m%d')}.log")

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler(log_file, encoding='utf-8')  # 输出到文件
    ]
)

# 获取应用的logger
logger = logging.getLogger(__name__)
logger.info(f"日志文件位置: {log_file}")

# 配置uvicorn访问日志
uvicorn_access_logger = logging.getLogger("uvicorn.access")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
uvicorn_access_logger.handlers = [handler]

###################
# FastAPI 应用配置
###################

# 创建FastAPI应用
app = FastAPI(
    title="AI 文章生成器",
    description="""
    这是一个基于Monica AI的智能文章生成工具。

    ## 功能特点
    * 自动生成文章
    * 智能标题生成
    * 多种写作风格

    ## 使用方法
    1. 调用生成API
    2. 获取生成结果
    """,
    version="1.0.0",
    contact={
        "name": "技术支持",
        "email": "wanghaokunlink@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "文章生成",
            "description": "文章生成相关的API接口",
        }
    ]
)

# 配置CORS
try:
    # 尝试解析JSON格式的允许源列表
    allowed_origins = json.loads(os.getenv("ALLOWED_ORIGINS", "[]"))
    if not isinstance(allowed_origins, list) or not allowed_origins:
        allowed_origins = ["*"]
except json.JSONDecodeError:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###################
# 路由配置
###################

# 注册路由
app.include_router(article.router, prefix="/blog")

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "欢迎使用博客生成器 API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

###################
# 中间件配置
###################

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """请求日志中间件"""
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
