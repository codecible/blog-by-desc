from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "操作成功",
                "data": {"key": "value"}
            }
        },
        protected_namespaces=()
    ) 