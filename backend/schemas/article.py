from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from .base import BaseResponse

class ArticleRequest(BaseModel):
    """
    文章生成请求模型
    
    用于验证和规范化用户提交的文章生成请求数据
    包含文章的描述信息和可选的核心主题
    """
    description: str = Field(
        ...,  # 表示必填字段
        min_length=5,  # 最小长度限制
        max_length=1000,  # 最大长度限制
        description="文章的主要描述内容，用于指导AI生成文章"
    )
    core_idea: Optional[str] = Field(
        None,  # 默认值为None，表示选填
        max_length=100,  # 最大长度限制
        description="文章的核心主题，用于确定文章的中心思想"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "探讨人工智能对未来教育的影响",
                "core_idea": "AI教育革命"
            }
        }
    )

class ArticleData(BaseModel):
    """文章数据模型"""
    title: str = Field(..., description="生成的文章标题")
    content: str = Field(..., description="生成的文章内容")
    directions: List[str] = Field(..., description="文章的写作方向列表")
    file_path: str = Field(..., description="文章保存的文件路径")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "揭秘AI如何定制个性化学习，提升学生成绩的3大关键",
                "content": "# 揭秘AI如何定制个性化学习...",
                "directions": [
                    "个性化学习：AI如何根据学生需求定制教育内容",
                    "教师角色转变：AI在课堂中的辅助与替代",
                    "未来技能培养：AI时代需要的核心素养"
                ],
                "file_path": "output/202312211234.md"
            }
        }
    )

class ArticleResponse(BaseResponse):
    """
    文章生成响应模型
    
    继承自BaseResponse，用于规范化API响应格式
    包含生成的文章信息，如标题、内容、写作方向等
    """
    success: bool = Field(
        True,
        description="请求是否成功"
    )
    message: Optional[str] = Field(
        None,
        description="响应消息"
    )
    data: Optional[ArticleData] = Field(
        None,
        description="文章数据"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "文章生成成功",
                "data": {
                    "title": "揭秘AI如何定制个性化学习，提升学生成绩的3大关键",
                    "content": "# 揭秘AI如何定制个性化学习...",
                    "directions": [
                        "个性化学习：AI如何根据学生需求定制教育内容",
                        "教师角色转变：AI在课堂中的辅助与替代",
                        "未来技能培养：AI时代需要的核心素养"
                    ],
                    "file_path": "output/202312211234.md"
                }
            }
        }
    ) 