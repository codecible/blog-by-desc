from fastapi import APIRouter, HTTPException
from backend.schemas.article import ArticleRequest, ArticleResponse
from backend.services.article_generator import ArticleGenerator

class ArticleController:
    """文章控制器：处理文章相关的HTTP请求"""
    
    def __init__(self):
        self.router = APIRouter(
            prefix="/blog",
            tags=["blog"],
            responses={404: {"description": "Not found"}},
        )
        self._register_routes()
        
    def _register_routes(self):
        """注册路由处理器"""
        self.router.add_api_route(
            "/generate",
            self.generate_article,
            methods=["POST"],
            response_model=ArticleResponse,
            summary="生成文章",
            description="根据提供的描述和核心主题生成文章"
        )
    
    async def generate_article(self, request: ArticleRequest) -> ArticleResponse:
        """
        生成文章的API接口
        
        Args:
            request: 包含文章描述和核心主题的请求对象
            
        Returns:
            ArticleResponse: 包含生成的文章信息的响应对象
            
        Raises:
            HTTPException: 当文章生成过程中发生错误时抛出
        """
        generator = ArticleGenerator()
        
        try:
            return await generator.generate(request)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"生成文章失败: {str(e)}"
            ) 