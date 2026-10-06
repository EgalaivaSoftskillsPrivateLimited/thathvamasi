"""
Security utilities and middleware
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token handling
security = HTTPBearer()

limiter = Limiter(key_func=get_remote_address)

def setup_security(app: FastAPI):
    """
    Setup security middleware for the application
    """
    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verify and decode JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
        return payload
        
    except JWTError:
        raise credentials_exception

async def get_current_user(
    payload: Dict[str, Any] = Depends(verify_token),
):
    """
    Get current user from token payload
    """
    from app.models.user_model import User
    from app.core.database import AsyncSessionLocal
    from sqlalchemy import select
    
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    async with AsyncSessionLocal() as db:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

def check_admin_permissions(user = Depends(get_current_user)):
    """
    Check if user has admin permissions
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return user

def generate_reset_token() -> str:
    """
    Generate a password reset token
    """
    return secrets.token_urlsafe(32)

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal
    """
    import re
    # Remove directory paths
    filename = os.path.basename(filename)
    # Remove special characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename

def validate_file_type(file_content_type: str) -> bool:
    """
    Validate file type against allowed types
    """
    return file_content_type in settings.ALLOWED_FILE_TYPES

def validate_file_size(file_size: int) -> bool:
    """
    Validate file size against maximum limit
    """
    return file_size <= settings.MAX_UPLOAD_SIZE

# Rate limiting decorators
rate_limit_public = limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
rate_limit_auth = limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE//2}/minute")
rate_limit_strict = limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE//10}/minute")

import os
# Note: os is imported here for sanitize_filename function