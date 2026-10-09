"""
SQLAlchemy Contact Enquiry model for Thathvamasi HR Consultancy
"""

import uuid
from sqlalchemy import Column, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base


class ContactEnquiry(Base):
    """
    General and service enquiries from the website
    """
    __tablename__ = "contact_enquiries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(50), nullable=True)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="new", nullable=False)  # new, contacted, resolved, closed
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        Index('ix_contact_enquiries_email', 'email'),
        Index('ix_contact_enquiries_status', 'status'),
        Index('ix_contact_enquiries_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<ContactEnquiry(id={self.id}, name={self.name}, email={self.email})>"
