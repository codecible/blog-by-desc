from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ArticleRequest(BaseModel):
    """文章生成请求模型"""
    description: str
    core_idea: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "探讨人工智能对未来教育的影响",
                "core_idea": "AI教育革命"
            }
        }
    )

class ArticleResponse(BaseModel):
    """文章生成响应模型"""
    title: str
    content: str
    directions: List[str]
    file_path: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "AI教育革命：5大变革重塑未来课堂",
                "content": "文章内容...",
                "directions": ["方向1", "方向2", "方向3"],
                "file_path": "output/202312211234.md"
            }
        }
    ) 