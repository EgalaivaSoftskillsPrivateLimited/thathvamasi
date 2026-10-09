"""
Client/Employer models for Thathvamasi HR Consultancy
"""

from typing import Optional, List
from pydantic import Field, validator, EmailStr
from app.models.base import BaseDBModel
from app.utils.helpers import validate_indian_mobile


class CompanyInfo(BaseDBModel):
    """
    Company information model
    """
    company_name: str = Field(..., min_length=2, max_length=200, description="Company name")
    contact_person: str = Field(..., min_length=2, max_length=100, description="Contact person name")
    designation: Optional[str] = Field(None, max_length=100, description="Designation of contact person")
    email: EmailStr = Field(..., description="Official email address")
    mobile: str = Field(..., description="Mobile number")
    company_location: Optional[str] = Field(None, max_length=200, description="Company location")
    company_website: Optional[str] = Field(None, description="Company website URL")
    industry: Optional[str] = Field(None, max_length=100, description="Industry/sector")
    company_size: Optional[str] = Field(None, description="Company size (e.g., '1-50', '51-200', '201-500', '500+')")
    company_type: Optional[str] = Field(None, description="Company type (Private, Public, MNC, Startup, etc.)")
    
    @validator('mobile')
    def validate_mobile(cls, v):
        if not validate_indian_mobile(v):
            raise ValueError('Invalid Indian mobile number format')
        return v
    
    @validator('company_website')
    def validate_website(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v


class HiringRequirement(BaseDBModel):
    """
    Hiring requirement model
    """
    position_title: str = Field(..., min_length=2, max_length=100, description="Position/job title")
    number_of_vacancies: int = Field(..., ge=1, description="Number of vacancies")
    job_location: str = Field(..., min_length=2, max_length=200, description="Job location")
    required_experience: Optional[str] = Field(None, description="Required experience (e.g., '2-5 years')")
    required_qualification: Optional[str] = Field(None, max_length=100, description="Required qualification")
    key_skills: List[str] = Field(default_factory=list, description="Key skills required")
    salary_range: Optional[str] = Field(None, description="Salary/CTC range (e.g., '10-15 LPA')")
    employment_type: Optional[str] = Field(default="Permanent", description="Employment type")
    expected_joining_timeline: Optional[str] = Field(None, description="Expected joining timeline")
    job_description: Optional[str] = Field(None, description="Job description")
    additional_requirements: Optional[str] = Field(None, description="Additional requirements")
    
    @validator('employment_type')
    def validate_employment_type(cls, v):
        allowed_types = ['Permanent', 'Contract', 'Temporary', 'Internship', 'Part-time']
        if v not in allowed_types:
            raise ValueError(f'Employment type must be one of: {", ".join(allowed_types)}')
        return v


class JobDescriptionFile(BaseDBModel):
    """
    Job description file model
    """
    url: Optional[str] = Field(None, description="JD file URL")
    file_name: Optional[str] = Field(None, description="Original file name")
    file_size: Optional[int] = Field(None, ge=0, description="File size in bytes")
    file_type: Optional[str] = Field(None, description="File type (pdf, doc, docx)")
    cloudinary_id: Optional[str] = Field(None, description="Cloudinary public ID")


class ClientMetadata(BaseDBModel):
    """
    Client metadata model
    """
    ip_address: Optional[str] = Field(None, description="IP address of submission")
    user_agent: Optional[str] = Field(None, description="User agent string")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    source: Optional[str] = Field(None, description="Source of enquiry")
    device_type: Optional[str] = Field(None, description="Device type")


class Client(BaseDBModel):
    """
    Complete client model
    """
    company_info: CompanyInfo
    hiring_requirement: HiringRequirement
    job_description_file: Optional[JobDescriptionFile] = Field(None, description="Uploaded JD file")
    
    # Status fields
    status: str = Field(default="new", description="Client enquiry status")
    status_changed_at: Optional[str] = Field(None, description="When status was last changed")
    status_notes: Optional[str] = Field(None, description="Notes about status change")
    
    # Follow-up fields
    follow_up_date: Optional[str] = Field(None, description="Next follow-up date")
    follow_up_notes: Optional[str] = Field(None, description="Follow-up notes")
    assigned_to: Optional[str] = Field(None, description="Admin user assigned to this client")
    
    # Metadata
    metadata: Optional[ClientMetadata] = Field(None, description="Submission metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "company_info": {
                    "company_name": "ABC Corporation",
                    "contact_person": "Jane Smith",
                    "designation": "HR Manager",
                    "email": "jane.smith@abccorp.com",
                    "mobile": "9876543210",
                    "company_location": "Coimbatore",
                    "company_website": "https://abccorp.com",
                    "industry": "IT Services"
                },
                "hiring_requirement": {
                    "position_title": "Software Developer",
                    "number_of_vacancies": 3,
                    "job_location": "Coimbatore",
                    "required_experience": "2-5 years",
                    "required_qualification": "BE/B.Tech in CS/IT",
                    "key_skills": ["Python", "Django", "React", "PostgreSQL"],
                    "salary_range": "8-12 LPA",
                    "employment_type": "Permanent",
                    "expected_joining_timeline": "Immediate to 30 days"
                },
                "status": "new"
            }
        }


class ClientCreate(BaseDBModel):
    """
    Model for creating a new client enquiry
    """
    company_info: CompanyInfo
    hiring_requirement: HiringRequirement
    
    class Config:
        schema_extra = {
            "example": {
                "company_info": {
                    "company_name": "ABC Corporation",
                    "contact_person": "Jane Smith",
                    "email": "jane.smith@abccorp.com",
                    "mobile": "9876543210"
                },
                "hiring_requirement": {
                    "position_title": "Software Developer",
                    "number_of_vacancies": 3,
                    "job_location": "Coimbatore"
                }
            }
        }


class ClientUpdate(BaseDBModel):
    """
    Model for updating client information
    """
    status: Optional[str] = None
    status_notes: Optional[str] = None
    follow_up_date: Optional[str] = None
    follow_up_notes: Optional[str] = None
    assigned_to: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "contacted",
                "status_notes": "Initial discussion completed",
                "follow_up_date": "2026-10-12",
                "assigned_to": "admin@thathvamasi.com"
            }
        }


class ClientResponse(BaseDBModel):
    """
    Client response model for API
    """
    client: Client
    success: bool = True
    message: Optional[str] = None


class ClientsListResponse(BaseDBModel):
    """
    List of clients response model
    """
    clients: List[Client]
    total: int
    page: int = 1
    limit: int = 10
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    success: bool = True


class ClientStatusCount(BaseDBModel):
    """
    Client status count model for analytics
    """
    status: str
    count: int


class ClientAnalytics(BaseDBModel):
    """
    Client analytics model
    """
    total_clients: int
    status_counts: List[ClientStatusCount]
    new_this_month: int
    new_this_week: int
    avg_response_time_hours: Optional[float] = None
    conversion_rate: Optional[float] = None