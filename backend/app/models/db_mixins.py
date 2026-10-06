"""
SQLAlchemy database mixins for common fields
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, func, Boolean, String
from sqlalchemy.orm import declared_attr
import uuid


class TimestampMixin:
    """
    Mixin for created_at and updated_at timestamps
    """
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class UUIDMixin:
    """
    Mixin for UUID primary key
    """
    @declared_attr
    def id(cls):
        from sqlalchemy.dialects.postgresql import UUID
        return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class SoftDeleteMixin:
    """
    Mixin for soft delete functionality
    """
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def soft_delete(self):
        """Soft delete the record"""
        self.deleted_at = datetime.utcnow()
        self.is_deleted = True
    
    def restore(self):
        """Restore a soft-deleted record"""
        self.deleted_at = None
        self.is_deleted = False


class AuditMixin:
    """
    Mixin for audit trail
    """
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)