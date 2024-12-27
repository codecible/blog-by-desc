"""
文章相关的数据模型

这个模块定义了与文章生成相关的所有数据模型。
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from .base import BaseResponse

# 定义支持的模型类型
ModelType = Literal["monica", "zhipu"]

class ArticleRequest(BaseModel):
    """
    文章生成请求模型
    
    用于验证和规范化用户的文章生成请求
    """
    description: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="文章描述，用于生成文章的主要输入"
    )
    core_idea: Optional[str] = Field(
        None,
        max_length=100,
        description="核心主题，用于指导文章生成的方向"
    )
    model_type: ModelType = Field(
        "monica",
        description="AI模型类型，支持'monica'和'zhipu'"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "写一篇关于人工智能在教育领域应用的文章",
                "core_idea": "AI如何改变传统教育模式",
                "model_type": "monica"
            }
        },
        protected_namespaces=()
    )

class ArticleData(BaseModel):
    """
    文章数据模型
    
    用于存储生成的文章信息
    """
    title: str = Field(
        ...,
        description="文章标题"
    )
    content: str = Field(
        ...,
        description="文章内容"
    )
    directions: List[str] = Field(
        ...,
        description="写作方向列表"
    )
    file_path: str = Field(
        ...,
        description="文章保存的文件路径"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "AI教育革命：改变未来课堂的三大方向",
                "content": "# AI教育革命：改变未来课堂的三大方向\n\n## 引言\n\n...",
                "directions": [
                    "AI个性化学习",
                    "智能教学助手",
                    "教育资源优化"
                ],
                "file_path": "output/202312201234.md"
            }
        },
        protected_namespaces=()
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
        },
        protected_namespaces=()
    ) 