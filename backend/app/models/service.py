"""
Service models for Thathvamasi HR Consultancy
"""

from typing import Optional, List
from pydantic import Field
from app.models.base import BaseDBModel
from app.utils.helpers import generate_slug


class ServiceFeature(BaseDBModel):
    """
    Service feature model
    """
    title: str = Field(..., min_length=2, max_length=100, description="Feature title")
    description: Optional[str] = Field(None, description="Feature description")
    icon: Optional[str] = Field(None, description="Feature icon")
    order: int = Field(default=0, description="Display order")


class ServiceBenefit(BaseDBModel):
    """
    Service benefit model
    """
    title: str = Field(..., min_length=2, max_length=100, description="Benefit title")
    description: Optional[str] = Field(None, description="Benefit description")
    icon: Optional[str] = Field(None, description="Benefit icon")


class ServiceFAQ(BaseDBModel):
    """
    Service FAQ model
    """
    question: str = Field(..., min_length=5, max_length=200, description="FAQ question")
    answer: str = Field(..., min_length=10, description="FAQ answer")
    order: int = Field(default=0, description="Display order")


class ServiceSEO(BaseDBModel):
    """
    Service SEO metadata
    """
    meta_title: Optional[str] = Field(None, max_length=60, description="SEO meta title")
    meta_description: Optional[str] = Field(None, max_length=160, description="SEO meta description")
    meta_keywords: Optional[List[str]] = Field(default_factory=list, description="SEO keywords")


class Service(BaseDBModel):
    """
    Complete service model
    """
    name: str = Field(..., min_length=2, max_length=100, description="Service name")
    slug: str = Field(..., description="Service URL slug")
    short_description: str = Field(..., max_length=200, description="Short description")
    long_description: str = Field(..., description="Detailed description")
    icon: Optional[str] = Field(None, description="Service icon")
    image: Optional[str] = Field(None, description="Service image URL")
    
    # Categorization
    category: Optional[str] = Field(None, description="Service category")
    tags: List[str] = Field(default_factory=list, description="Service tags")
    
    # Features and benefits
    features: List[ServiceFeature] = Field(default_factory=list, description="Service features")
    benefits: List[ServiceBenefit] = Field(default_factory=list, description="Service benefits")
    faqs: List[ServiceFAQ] = Field(default_factory=list, description="Frequently asked questions")
    
    # Display and ordering
    order: int = Field(default=0, description="Display order")
    is_featured: bool = Field(default=False, description="Whether service is featured")
    is_active: bool = Field(default=True, description="Whether service is active")
    
    # SEO
    seo: Optional[ServiceSEO] = Field(None, description="SEO metadata")
    
    # Statistics
    view_count: int = Field(default=0, description="Number of views")
    enquiry_count: int = Field(default=0, description="Number of enquiries")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Recruitment & Talent Acquisition",
                "slug": "recruitment-talent-acquisition",
                "short_description": "End-to-end recruitment solutions for businesses",
                "long_description": "We provide comprehensive recruitment services...",
                "icon": "recruitment",
                "category": "Staffing",
                "tags": ["recruitment", "talent", "hiring"],
                "order": 1,
                "is_featured": True,
                "is_active": True,
                "features": [
                    {
                        "title": "Candidate Sourcing",
                        "description": "Wide network of qualified candidates"
                    }
                ],
                "benefits": [
                    {
                        "title": "Time Saving",
                        "description": "Reduce hiring time by 50%"
                    }
                ]
            }
        }


class ServiceCreate(BaseDBModel):
    """
    Model for creating a new service
    """
    name: str = Field(..., min_length=2, max_length=100)
    short_description: str = Field(..., max_length=200)
    long_description: str = Field(...)
    icon: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    order: Optional[int] = 0
    is_featured: Optional[bool] = False
    is_active: Optional[bool] = True
    
    # SEO fields
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)
    meta_keywords: Optional[List[str]] = None
    
    @validator('slug', pre=True, always=True)
    def generate_slug_from_name(cls, v, values):
        if 'name' in values and values['name']:
            return generate_slug(values['name'])
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Recruitment & Talent Acquisition",
                "short_description": "End-to-end recruitment solutions",
                "long_description": "Comprehensive recruitment services...",
                "category": "Staffing",
                "tags": ["recruitment", "hiring"],
                "order": 1,
                "is_featured": True
            }
        }


class ServiceUpdate(BaseDBModel):
    """
    Model for updating a service
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    short_description: Optional[str] = Field(None, max_length=200)
    long_description: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    order: Optional[int] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    
    # SEO fields
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)
    meta_keywords: Optional[List[str]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Updated Recruitment Services",
                "short_description": "Enhanced recruitment solutions",
                "is_featured": True
            }
        }


class ServiceResponse(BaseDBModel):
    """
    Service response model for API
    """
    service: Service
    success: bool = True
    message: Optional[str] = None


class ServicesListResponse(BaseDBModel):
    """
    List of services response model
    """
    services: List[Service]
    total: int
    page: int = 1
    limit: int = 10
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    success: bool = True


class ServiceCategory(BaseDBModel):
    """
    Service category model
    """
    name: str = Field(..., min_length=2, max_length=50, description="Category name")
    slug: str = Field(..., description="Category slug")
    description: Optional[str] = Field(None, description="Category description")
    icon: Optional[str] = Field(None, description="Category icon")
    order: int = Field(default=0, description="Display order")
    is_active: bool = Field(default=True, description="Whether category is active")
    service_count: int = Field(default=0, description="Number of services in this category")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Staffing Solutions",
                "slug": "staffing-solutions",
                "description": "Complete staffing and recruitment solutions",
                "icon": "staffing",
                "order": 1,
                "service_count": 3
            }
        }


class ServiceStats(BaseDBModel):
    """
    Service statistics model
    """
    total_services: int
    active_services: int
    featured_services: int
    total_views: int
    total_enquiries: int
    categories_count: int
    most_viewed_service: Optional[str] = None
    most_viewed_count: Optional[int] = None
    most_enquired_service: Optional[str] = None
    most_enquired_count: Optional[int] = None


class ServiceEnquiry(BaseDBModel):
    """
    Service-specific enquiry model
    """
    service_id: str = Field(..., description="Service ID")
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    company: Optional[str] = Field(None, max_length=200, description="Company name")
    email: EmailStr = Field(..., description="Email address")
    mobile: str = Field(..., description="Mobile number")
    message: str = Field(..., min_length=10, max_length=1000, description="Enquiry message")
    enquiry_date: Optional[str] = Field(None, description="Enquiry date")
    status: str = Field(default="new", description="Enquiry status")
    
    class Config:
        schema_extra = {
            "example": {
                "service_id": "service_123",
                "name": "John Smith",
                "company": "Tech Solutions",
                "email": "john@techsolutions.com",
                "mobile": "9876543210",
                "message": "Interested in your recruitment services...",
                "status": "new"
            }
        }


from pydantic import EmailStr