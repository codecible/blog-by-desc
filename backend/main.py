import os
import json
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import datetime

from backend.routers import article

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 获取应用的logger
logger = logging.getLogger(__name__)

# 获取 uvicorn 的访问日志记录器并设置格式
uvicorn_access_logger = logging.getLogger("uvicorn.access")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
uvicorn_access_logger.handlers = [handler]

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

# 从环境变量获取CORS配置
try:
    # 尝试解析JSON格式的允许源列表
    allowed_origins = json.loads(os.getenv("ALLOWED_ORIGINS", "[]"))
    # 确保是列表类型
    if not isinstance(allowed_origins, list):
        allowed_origins = ["*"]
    # 确保列表不为空
    if not allowed_origins:
        allowed_origins = ["*"]
except json.JSONDecodeError:
    # 如果解析失败，默认允许所有源
    allowed_origins = ["*"]

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response