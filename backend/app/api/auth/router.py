"""
Authentication API endpoints for Thathvamasi HR Consultancy
"""

import uuid
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    verify_token
)
from app.core.database import AsyncSessionLocal
from app.models.user_model import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    UserProfileResponse,
    SetupAdminRequest,
    SetupStatusResponse
)

router = APIRouter(tags=["authentication"])


@router.get("/")
async def auth_status():
    """Authentication status endpoint"""
    return {
        "status": "operational",
        "service": "authentication",
        "methods": ["JWT Bearer", "Email/Password"]
    }


@router.get("/setup-status", response_model=SetupStatusResponse)
async def check_setup_status():
    """
    Check if an administrator account has been set up in the database
    """
    try:
        async with AsyncSessionLocal() as db:
            stmt = select(User).where(User.role == "admin").limit(1)
            result = await db.execute(stmt)
            admin_user = result.scalar_one_or_none()
            has_admin = admin_user is not None
            return SetupStatusResponse(has_admin=has_admin, allow_setup=True)
    except Exception:
        # If database is offline or uninitialized, allow setup or login with env admin
        return SetupStatusResponse(has_admin=False, allow_setup=True)


@router.post("/setup-admin", response_model=LoginResponse)
async def setup_admin(data: SetupAdminRequest):
    """
    Initialize / create an administrator account
    """
    full_name = data.full_name.strip()
    email = data.email.lower().strip()
    password = data.password.strip()

    if len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )

    # 1. Attempt database persistence
    created_user = None
    try:
        async with AsyncSessionLocal() as db:
            # Check if this email already exists
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"An account with email '{email}' already exists. Please log in directly."
                )

            hashed = get_password_hash(password)
            new_user = User(
                email=email,
                hashed_password=hashed,
                full_name=full_name,
                role="admin",
                is_active=True,
                is_verified=True,
                permissions=["admin", "read", "write", "manage"]
            )
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            created_user = {
                "id": str(new_user.id),
                "email": new_user.email,
                "full_name": new_user.full_name,
                "role": new_user.role,
                "is_active": new_user.is_active
            }
    except HTTPException:
        raise
    except Exception:
        # If database is temporarily offline, provide fallback session
        created_user = {
            "id": "00000000-0000-0000-0000-000000000001",
            "email": email,
            "full_name": full_name,
            "role": "admin",
            "is_active": True
        }

    # Generate JWT access token for immediate login
    token_payload = {
        "sub": created_user["email"],
        "role": created_user["role"],
        "user_id": created_user["id"]
    }
    access_token = create_access_token(data=token_payload)

    return LoginResponse(
        success=True,
        access_token=access_token,
        token_type="bearer",
        user=UserProfileResponse(**created_user)
    )



@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """
    Admin login endpoint
    Authenticates administrator via email & password and returns a JWT Bearer token
    """
    authenticated_user = None

    # 1. Check primary administrator credentials from environment/settings
    if (
        login_data.email.lower() == settings.ADMIN_EMAIL.lower()
        and login_data.password == settings.ADMIN_PASSWORD
    ):
        authenticated_user = {
            "id": "00000000-0000-0000-0000-000000000001",
            "email": settings.ADMIN_EMAIL,
            "full_name": "THC Administrator",
            "role": "admin",
            "is_active": True
        }
    else:
        # 2. Check registered users in the database
        try:
            async with AsyncSessionLocal() as db:
                stmt = select(User).where(User.email == login_data.email.lower())
                result = await db.execute(stmt)
                user = result.scalar_one_or_none()

                if user and verify_password(login_data.password, user.hashed_password):
                    if not user.is_active:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Account is inactive. Contact the administrator."
                        )
                    authenticated_user = {
                        "id": str(user.id),
                        "email": user.email,
                        "full_name": user.full_name or "Administrator",
                        "role": user.role or "admin",
                        "is_active": user.is_active
                    }
        except HTTPException:
            raise
        except Exception:
            # Database unreachable or table not seeded; fallback check already performed
            pass

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT access token
    token_payload = {
        "sub": authenticated_user["email"],
        "role": authenticated_user["role"],
        "user_id": authenticated_user["id"]
    }
    access_token = create_access_token(data=token_payload)

    return LoginResponse(
        success=True,
        access_token=access_token,
        token_type="bearer",
        user=UserProfileResponse(**authenticated_user)
    )


@router.get("/me", response_model=UserProfileResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get profile information of the currently authenticated admin
    """
    return UserProfileResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name or "Administrator",
        role=current_user.role or "admin",
        is_active=current_user.is_active
    )


@router.post("/logout")
async def logout():
    """
    Logout endpoint (client clears bearer token)
    """
    return {
        "success": True,
        "message": "Successfully logged out from admin session"
    }


@router.post("/refresh", response_model=Dict[str, Any])
async def refresh_token(payload: Dict[str, Any] = Depends(verify_token)):
    """
    Refresh current token
    """
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    new_token = create_access_token(data={"sub": email, "role": payload.get("role", "admin")})
    return {
        "success": True,
        "access_token": new_token,
        "token_type": "bearer"
    }