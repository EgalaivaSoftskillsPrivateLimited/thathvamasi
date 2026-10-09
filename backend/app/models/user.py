"""
User models for authentication and authorization
"""

from typing import Optional, List
from datetime import datetime
from pydantic import Field, validator, EmailStr
from app.models.base import BaseDBModel
from app.utils.helpers import validate_email


class UserBase(BaseDBModel):
    """
    Base user model
    """
    email: EmailStr = Field(..., description="Email address")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name")
    is_active: bool = Field(default=True, description="Whether user account is active")
    role: str = Field(default="user", description="User role")
    
    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ['admin', 'editor', 'viewer', 'user']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v


class UserCreate(UserBase):
    """
    Model for creating a new user
    """
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., description="Confirm password")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        # Check password strength
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "email": "admin@thathvamasi.com",
                "full_name": "Administrator",
                "password": "Admin@123",
                "confirm_password": "Admin@123",
                "role": "admin"
            }
        }


class UserLogin(BaseDBModel):
    """
    Model for user login
    """
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")
    remember_me: bool = Field(default=False, description="Remember login session")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "admin@thathvamasi.com",
                "password": "Admin@123"
            }
        }


class UserUpdate(BaseDBModel):
    """
    Model for updating user information
    """
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    is_active: Optional[bool] = None
    role: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "Updated Name",
                "is_active": True,
                "role": "editor"
            }
        }


class UserPasswordChange(BaseDBModel):
    """
    Model for changing password
    """
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('New passwords do not match')
        return v
    
    @validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "current_password": "OldPassword@123",
                "new_password": "NewPassword@123",
                "confirm_password": "NewPassword@123"
            }
        }


class User(UserBase):
    """
    Complete user model (database representation)
    """
    hashed_password: str = Field(..., description="Hashed password")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    login_count: int = Field(default=0, description="Number of logins")
    
    # Profile fields
    phone: Optional[str] = Field(None, description="Phone number")
    designation: Optional[str] = Field(None, description="Designation/role in company")
    department: Optional[str] = Field(None, description="Department")
    avatar: Optional[str] = Field(None, description="Avatar URL")
    
    # Security
    is_verified: bool = Field(default=False, description="Whether email is verified")
    verification_token: Optional[str] = Field(None, description="Email verification token")
    reset_token: Optional[str] = Field(None, description="Password reset token")
    reset_token_expires: Optional[datetime] = Field(None, description="Reset token expiry")
    
    # Preferences
    preferences: Optional[dict] = Field(default_factory=dict, description="User preferences")
    
    # Permissions
    permissions: List[str] = Field(default_factory=list, description="User permissions")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "admin@thathvamasi.com",
                "full_name": "Administrator",
                "role": "admin",
                "is_active": True,
                "hashed_password": "$2b$12$...",
                "login_count": 42,
                "last_login": "2026-10-05T10:30:00Z"
            }
        }


class UserProfile(BaseDBModel):
    """
    User profile model for API responses (without sensitive data)
    """
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    last_login: Optional[datetime] = None
    login_count: int = 0
    phone: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    avatar: Optional[str] = None
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "email": "admin@thathvamasi.com",
                "full_name": "Administrator",
                "role": "admin",
                "is_active": True,
                "login_count": 42,
                "last_login": "2026-10-05T10:30:00Z",
                "created_at": "2026-10-01T00:00:00Z"
            }
        }


class Token(BaseDBModel):
    """
    Authentication token model
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiry in seconds")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "expires_in": 604800,
                "refresh_token": "refresh_token_here"
            }
        }


class TokenData(BaseDBModel):
    """
    Token data payload model
    """
    sub: Optional[str] = Field(None, description="Subject (usually user email)")
    exp: Optional[datetime] = Field(None, description="Expiration time")
    role: Optional[str] = Field(None, description="User role")


class UserResponse(BaseDBModel):
    """
    User response model for API
    """
    user: UserProfile
    success: bool = True
    message: Optional[str] = None


class UsersListResponse(BaseDBModel):
    """
    List of users response model
    """
    users: List[UserProfile]
    total: int
    page: int = 1
    limit: int = 10
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    success: bool = True


class PasswordResetRequest(BaseDBModel):
    """
    Password reset request model
    """
    email: EmailStr = Field(..., description="Email address")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "admin@thathvamasi.com"
            }
        }


class PasswordResetConfirm(BaseDBModel):
    """
    Password reset confirmation model
    """
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "token": "reset_token_here",
                "new_password": "NewPassword@123",
                "confirm_password": "NewPassword@123"
            }
        }


class UserActivity(BaseDBModel):
    """
    User activity log model
    """
    user_id: str = Field(..., description="User ID")
    activity_type: str = Field(..., description="Type of activity")
    description: str = Field(..., description="Activity description")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)