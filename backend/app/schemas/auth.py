"""
Authentication schemas for Thathvamasi HR Consultancy API
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Admin login request schema"""
    email: EmailStr = Field(..., description="Administrator email address")
    password: str = Field(..., min_length=1, description="Account password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "admin@thathvamasi.com",
                "password": "admin123"
            }
        }
    }


class UserProfileResponse(BaseModel):
    """User profile response schema"""
    id: str = Field(..., description="User identifier")
    email: str = Field(..., description="Email address")
    full_name: str = Field(..., description="Full display name")
    role: str = Field("admin", description="Access role")
    is_active: bool = Field(True, description="Active status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "00000000-0000-0000-0000-000000000001",
                "email": "admin@thathvamasi.com",
                "full_name": "THC Administrator",
                "role": "admin",
                "is_active": True
            }
        }
    }


class LoginResponse(BaseModel):
    """Login response with JWT token"""
    success: bool = True
    access_token: str = Field(..., description="JWT Bearer token")
    token_type: str = Field("bearer", description="Token type")
    user: UserProfileResponse = Field(..., description="Authenticated user info")

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "email": "admin@tbspltd.com",
                    "full_name": "THC Administrator",
                    "role": "admin",
                    "is_active": True
                }
            }
        }
    }

