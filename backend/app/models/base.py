"""
Base models and mixins for PostgreSQL database schemas
"""

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class BaseDBModel(BaseModel):
    """
    Base database model with common fields for PostgreSQL
    """
    id: Optional[UUID] = Field(default=None, description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Created timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Updated timestamp")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={UUID: str},
    )


class BaseResponseModel(BaseModel):
    """
    Base response model for API responses
    """
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None


class PaginatedResponse(BaseResponseModel):
    """
    Paginated response model
    """
    page: int = 1
    limit: int = 10
    total: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False


class ErrorResponse(BaseModel):
    """
    Error response model
    """
    success: bool = False
    error: str
    details: Optional[dict] = None
    code: Optional[str] = None