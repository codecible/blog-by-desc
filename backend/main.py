from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import article

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(article.router)

@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "欢迎使用博客生成器 API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }