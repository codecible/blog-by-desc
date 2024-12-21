from datetime import datetime
from typing import List, Optional
from uuid import uuid4

class Article:
    """
    文章数据模型
    
    注意：这是一个基础的数据模型，目前没有使用数据库。
    当需要数据库支持时，可以方便地转换为 SQLAlchemy 或其他 ORM 模型。
    """
    
    def __init__(
        self,
        title: str,
        content: str,
        directions: List[str],
        description: str,
        core_idea: Optional[str] = None
    ):
        self.id = str(uuid4())
        self.title = title
        self.content = content
        self.directions = directions
        self.description = description
        self.core_idea = core_idea
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "directions": self.directions,
            "description": self.description,
            "core_idea": self.core_idea,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> "Article":
        """从字典创建实例"""
        return cls(
            title=data["title"],
            content=data["content"],
            directions=data["directions"],
            description=data["description"],
            core_idea=data.get("core_idea")
        ) 