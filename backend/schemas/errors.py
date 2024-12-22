from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int
    message: str
    details: Optional[Any] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": 400,
                "message": "请求参数错误",
                "details": "文章描述不能为空"
            }
        }
    )

class ValidationError(ErrorResponse):
    """验证错误响应模型"""
    code: int = 400

class APIError(ErrorResponse):
    """API调用错误响应模型"""
    code: int = 500

class NotFoundError(ErrorResponse):
    """资源未找到错误响应模型"""
    code: int = 404 