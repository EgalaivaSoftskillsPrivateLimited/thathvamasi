"""
Base schemas for Thathvamasi HR Consultancy API
"""

from typing import Optional
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Schema for pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Page size")
    
    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "size": 20
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    error_code: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Resource not found",
                "error_code": "RESOURCE_NOT_FOUND"
            }
        }


class SuccessResponse(BaseModel):
    """Schema for success responses"""
    message: str
    data: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"}
            }
        }


class HealthCheckResponse(BaseModel):
    """Schema for health check responses"""
    status: str
    database: str
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "database": "connected",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }