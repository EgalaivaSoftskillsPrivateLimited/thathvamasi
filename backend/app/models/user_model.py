"""
SQLAlchemy User model for authentication and authorization
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ARRAY, Text, ForeignKey, Integer, Index
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base, declared_attr


class User(Base):
    """
    User model for authentication and authorization
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Personal information
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    designation = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Status and roles
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    role = Column(String(50), default="user", nullable=False)  # admin, editor, viewer, user
    permissions = Column(ARRAY(String), default=[], nullable=False)
    
    # Security
    verification_token = Column(String(255), nullable=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime(timezone=True), nullable=True)
    
    # Activity tracking
    last_login = Column(DateTime(timezone=True), nullable=True)
    login_count = Column(Integer, default=0, nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    # Preferences
    preferences = Column(JSON, default=dict, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    activities = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_users_email', 'email'),
        Index('ix_users_role', 'role'),
        Index('ix_users_is_active', 'is_active'),
        Index('ix_users_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class UserActivity(Base):
    """
    User activity log model
    """
    __tablename__ = "user_activities"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Activity details
    activity_type = Column(String(100), nullable=False)  # login, logout, password_change, etc.
    description = Column(Text, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    activity_metadata = Column(JSON, default=dict, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="activities")
    
    # Indexes
    __table_args__ = (
        Index('ix_user_activities_user_id', 'user_id'),
        Index('ix_user_activities_activity_type', 'activity_type'),
        Index('ix_user_activities_created_at', 'created_at'),
        Index('ix_user_activities_user_id_created_at', 'user_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<UserActivity(id={self.id}, user_id={self.user_id}, activity_type={self.activity_type})>"