from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from backend.schemas.article import ArticleRequest, ArticleResponse, ArticleData
from backend.schemas.errors import APIError
from backend.services.article_generator import ArticleGenerator

logger = logging.getLogger(__name__)

# 创建路由器实例
router = APIRouter(
    tags=["文章生成"]
)

@router.post("/generate")
async def generate_article(request: ArticleRequest):
    """
    生成文章的API接口

    处理流程：
    1. 接收包含文章描述和核心主题的请求
    2. 创建文章生成器实例
    3. 调用生成器的generate方法生成文章内容
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
                - content: 文章内容
                - file_path: 保存的文件路径

    Raises:
        HTTPException:
            - 500: 生成文章过程中发生错误
    """
    logger.info(f"Received generate request: {request}")
    # 创建文章生成器实例
    generator = ArticleGenerator()

    try:
        # 生成内容
        content = await generator.generate_content(
            request.description,
            request.core_idea
        )

        # 生成文件路径
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        file_path = f"output/{timestamp}.md"

        # 创建ArticleData实例
        article_data = ArticleData(
            content=content,
            file_path=file_path
        )

        # 将结果封装在响应模型中返回
        return ArticleResponse(
            success=True,
            message="文章生成成功",
            data=article_data
        )

    except Exception as e:
        logger.error(f"Error generating article: {e}")
        # 捕获所有异常并转换为HTTP 500错误
        raise HTTPException(
            status_code=500,
            detail=f"生成文章失败: {str(e)}"
        )
