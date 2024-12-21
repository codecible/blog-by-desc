from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controllers.article import ArticleController

app = FastAPI(
    title="博客生成器 API",
    description="基于AI的博客文章生成服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册控制器
article_controller = ArticleController()
app.include_router(article_controller.router)

@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "欢迎使用博客生成器 API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 