"""
Contact and general enquiry models
"""

from typing import Optional
from pydantic import Field, validator, EmailStr
from app.models.base import BaseDBModel
from app.utils.helpers import validate_indian_mobile


class ContactEnquiry(BaseDBModel):
    """
    Contact enquiry model
    """
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    company: Optional[str] = Field(None, max_length=200, description="Company name")
    email: EmailStr = Field(..., description="Email address")
    mobile: str = Field(..., description="Mobile number")
    subject: str = Field(..., min_length=2, max_length=200, description="Enquiry subject")
    message: str = Field(..., min_length=10, max_length=2000, description="Enquiry message")
    
    # Optional fields
    enquiry_type: Optional[str] = Field(default="general", description="Type of enquiry")
    preferred_contact: Optional[str] = Field(default="email", description="Preferred contact method")
    
    @validator('mobile')
    def validate_mobile(cls, v):
        if not validate_indian_mobile(v):
            raise ValueError('Invalid Indian mobile number format')
        return v
    
    @validator('enquiry_type')
    def validate_enquiry_type(cls, v):
        allowed_types = ['general', 'service', 'partnership', 'career', 'feedback', 'complaint']
        if v not in allowed_types:
            raise ValueError(f'Enquiry type must be one of: {", ".join(allowed_types)}')
        return v
    
    @validator('preferred_contact')
    def validate_preferred_contact(cls, v):
        allowed_methods = ['email', 'phone', 'whatsapp']
        if v not in allowed_methods:
            raise ValueError(f'Preferred contact must be one of: {", ".join(allowed_methods)}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith",
                "company": "Tech Solutions Ltd",
                "email": "john.smith@techsolutions.com",
                "mobile": "9876543210",
                "subject": "HR Consulting Services",
                "message": "I would like to know more about your HR consulting services...",
                "enquiry_type": "service",
                "preferred_contact": "email"
            }
        }


class ContactCreate(ContactEnquiry):
    """
    Model for creating a contact enquiry
    """
    pass


class ContactUpdate(BaseDBModel):
    """
    Model for updating contact enquiry status
    """
    status: Optional[str] = None
    response_notes: Optional[str] = None
    assigned_to: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "responded",
                "response_notes": "Sent service catalog via email",
                "assigned_to": "hr@thathvamasi.com"
            }
        }


class ContactMetadata(BaseDBModel):
    """
    Contact metadata model
    """
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    page_url: Optional[str] = Field(None, description="Page where form was submitted")
    
    class Config:
        schema_extra = {
            "example": {
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0...",
                "referrer": "https://www.google.com",
                "page_url": "https://thathvamasi.com/contact"
            }
        }


class Contact(BaseDBModel):
    """
    Complete contact model
    """
    name: str
    company: Optional[str] = None
    email: EmailStr
    mobile: str
    subject: str
    message: str
    enquiry_type: str = "general"
    preferred_contact: str = "email"
    
    # Status fields
    status: str = Field(default="new", description="Enquiry status")
    status_changed_at: Optional[str] = Field(None, description="When status was last changed")
    response_notes: Optional[str] = Field(None, description="Response notes")
    responded_at: Optional[str] = Field(None, description="When response was sent")
    assigned_to: Optional[str] = Field(None, description="Assigned to user")
    
    # Metadata
    metadata: Optional[ContactMetadata] = Field(None, description="Submission metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "mobile": "9876543210",
                "subject": "HR Services",
                "message": "Looking for HR consulting...",
                "status": "new",
                "enquiry_type": "service"
            }
        }


class ContactResponse(BaseDBModel):
    """
    Contact response model for API
    """
    contact: Contact
    success: bool = True
    message: Optional[str] = None


class ContactsListResponse(BaseDBModel):
    """
    List of contacts response model
    """
    contacts: List[Contact]
    total: int
    page: int = 1
    limit: int = 10
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    success: bool = True


class NewsletterSubscription(BaseDBModel):
    """
    Newsletter subscription model
    """
    email: EmailStr = Field(..., description="Email address")
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Name")
    subscribed_at: Optional[str] = Field(None, description="Subscription date")
    is_active: bool = Field(default=True, description="Whether subscription is active")
    subscription_source: Optional[str] = Field(None, description="Source of subscription")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "subscriber@example.com",
                "name": "John Doe",
                "subscription_source": "website footer"
            }
        }


class ContactAnalytics(BaseDBModel):
    """
    Contact analytics model
    """
    total_enquiries: int
    new_enquiries: int
    responded_enquiries: int
    pending_enquiries: int
    by_type: dict = Field(default_factory=dict, description="Enquiries by type")
    by_month: dict = Field(default_factory=dict, description="Enquiries by month")
    avg_response_time_hours: Optional[float] = None
    response_rate: Optional[float] = None


from typing import List