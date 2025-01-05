# 标准库导入
import datetime
import json
import logging
import os
import sys
from pathlib import Path

# 第三方库导入
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# 本地应用导入
from backend.routers import article
from backend.utils.paths import LOG_DIR

###################
# 日志配置
###################

# 生成日志文件名
log_file = os.path.join(LOG_DIR, f"{datetime.datetime.now().strftime('%Y%m%d')}.log")

# 根据环境设置日志级别
log_level = logging.INFO if os.getenv("ENVIRONMENT") == "production" else logging.DEBUG

# 配置日志格式
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler(log_file, encoding='utf-8')  # 输出到文件
    ]
)

# 获取应用的logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
logger.info(f"Setting log level to: {logging.getLevelName(log_level)}")
logger.info(f"日志文件位置: {log_file}")

# 配置uvicorn访问日志
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.setLevel(log_level)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
uvicorn_access_logger.handlers = [handler]

###################
# 初始化配置
###################

# 加载环境变量文件
def load_env_file():
    """加载环境变量文件"""
    current_dir = Path(__file__).resolve().parent
    env_file = current_dir / '.env'

    if env_file.exists():
        load_dotenv(env_file, override=True)
        logger.info(f"已加载环境变量文件: {env_file}")
    else:
        logger.warning("警告：未找到环境变量文件 .env")
        raise FileNotFoundError("未找到必需的环境变量文件 .env")

load_env_file()

# 设置 Python 路径
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

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
app.include_router(article.router, prefix="/article")

@app.get("/health")
async def health_check():
    """健康检查端点

    检查项目：
    1. 应用是否正常运行
    2. 日志目录是否可写
    3. 输出目录是否可写
    """
    try:
        # 检查日志目录是否可写
        log_dir = Path(LOG_DIR)
        if not log_dir.exists() or not os.access(log_dir, os.W_OK):
            logger.error("Health check failed: log directory is not writable")
            return {"status": "unhealthy", "detail": "log directory is not writable"}, 500

        # 检查输出目录是否可写
        output_dir = Path("output")
        if not output_dir.exists() or not os.access(output_dir, os.W_OK):
            logger.error("Health check failed: output directory is not writable")
            return {"status": "unhealthy", "detail": "output directory is not writable"}, 500

        # 所有检查都通过
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "detail": str(e)}, 500

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
    # 健康检查请求使用DEBUG级别日志
    if request.url.path == "/health":
        logger.debug(f"Health check request: {request.method} {request.url.path}")
        response = await call_next(request)
        # 只有在健康检查失败时才记录ERROR日志
        if response.status_code != 200:
            logger.error(f"Health check failed with status code: {response.status_code}")
        return response

    # 其他请求使用INFO级别日志
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
