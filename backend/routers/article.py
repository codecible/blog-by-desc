from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
from datetime import datetime

from ..schemas.article import ArticleRequest, ArticleResponse, ArticleData
from ..schemas.errors import APIError
from ..services.article_generator import ArticleGenerator

# 创建路由器实例，设置URL前缀和API标签
router = APIRouter(
    prefix="/blog",  # URL前缀，所有路由都会加上/blog
    tags=["文章生成"],  # Swagger UI中的分组标签
    responses={  # 默认的错误响应
        404: {"model": APIError, "description": "Not found"},  # 资源未找到
        500: {"model": APIError, "description": "Internal server error"}  # 服务器错误
    }
)

@router.post(
    "/generate",  # 路由路径：/blog/generate
    response_model=ArticleResponse,  # 响应数据模型
    summary="生成文章",  # API简要说明
    description="根据提供的描述和核心主题生成文章"  # API详细说明
)
async def generate_article(request: ArticleRequest) -> ArticleResponse:
    """
    生成文章的API接口
    
    处理流程：
    1. 接收包含文章描述和核心主题的请求
    2. 创建文章生成器实例
    3. 调用生成器的generate方法
    4. 返回生成的文章信息
    
    Args:
        request (ArticleRequest): 包含以下字段的请求对象
            - description: 文章描述（必填，5-1000字）
            - core_idea: 核心主题（选填，最多100字）
        
    Returns:
        ArticleResponse: 包含以下字段的响应对象
            - success: 是否成功
            - message: 响应消息
            - data: 包含文章信息的字典
                - title: 文章标题
                - content: 文章内容
                - directions: 写作方向列表
                - file_path: 保存的文件路径
        
    Raises:
        HTTPException: 
            - 500: 生成文章过程中发生错误
    """
    # 创建文章生成器实例
    generator = ArticleGenerator()
    
    try:
        # 生成写作方向
        directions = await generator.generate_directions(
            request.description,
            request.core_idea
        )
        
        # 生成标题
        title = await generator.generate_title(directions)
        
        # 生成内容
        content = await generator.generate_content(directions, title)
        
        # 生成文件路径
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        file_path = f"output/{timestamp}.md"
        
        # 创建ArticleData实例
        article_data = ArticleData(
            title=title,
            content=content,
            directions=directions,
            file_path=file_path
        )
        
        # 将结果封装在响应模型中返回
        return ArticleResponse(
            success=True,
            message="文章生成成功",
            data=article_data
        )
        
    except Exception as e:
        # 捕获所有异常并转换为HTTP 500错误
        raise HTTPException(
            status_code=500,
            detail=f"生成文章失败: {str(e)}"
        ) 