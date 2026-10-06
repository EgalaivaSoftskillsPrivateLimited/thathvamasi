"""
Candidate models for Thathvamasi HR Consultancy
"""

from typing import Optional, List
from datetime import date
from pydantic import Field, validator, EmailStr
from app.models.base import BaseDBModel
from app.utils.helpers import validate_indian_mobile


class CandidatePersonalDetails(BaseDBModel):
    """
    Candidate personal details model
    """
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name of the candidate")
    mobile: str = Field(..., description="Mobile number")
    whatsapp: Optional[str] = Field(None, description="WhatsApp number (optional)")
    email: EmailStr = Field(..., description="Email address")
    current_location: str = Field(..., min_length=2, max_length=100, description="Current location/city")
    preferred_location: Optional[str] = Field(None, min_length=2, max_length=100, description="Preferred job location")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    marital_status: Optional[str] = Field(None, description="Marital status")
    
    @validator('mobile')
    def validate_mobile(cls, v):
        if not validate_indian_mobile(v):
            raise ValueError('Invalid Indian mobile number format')
        return v
    
    @validator('whatsapp')
    def validate_whatsapp(cls, v):
        if v and not validate_indian_mobile(v):
            raise ValueError('Invalid Indian mobile number format for WhatsApp')
        return v


class CandidateProfessionalDetails(BaseDBModel):
    """
    Candidate professional details model
    """
    highest_qualification: str = Field(..., min_length=2, max_length=100, description="Highest qualification")
    specialization: Optional[str] = Field(None, max_length=100, description="Specialization/stream")
    total_experience: str = Field(..., description="Total work experience (e.g., '2 years', '5 months')")
    current_company: Optional[str] = Field(None, max_length=100, description="Current company")
    current_designation: Optional[str] = Field(None, max_length=100, description="Current designation")
    current_salary: Optional[float] = Field(None, ge=0, description="Current salary/CTC in INR")
    expected_salary: Optional[float] = Field(None, ge=0, description="Expected salary/CTC in INR")
    notice_period: Optional[str] = Field(None, description="Notice period (e.g., '15 days', '1 month')")
    skills: List[str] = Field(default_factory=list, description="List of key skills")
    preferred_job_role: Optional[str] = Field(None, max_length=100, description="Preferred job role/designation")
    industry: Optional[str] = Field(None, max_length=100, description="Industry/functional area")
    job_type_preference: Optional[str] = Field(None, description="Job type preference (Permanent, Contract, etc.)")
    languages_known: Optional[List[str]] = Field(default_factory=list, description="Languages known")


class CandidateResume(BaseDBModel):
    """
    Candidate resume model
    """
    url: str = Field(..., description="Resume file URL")
    file_name: str = Field(..., description="Original file name")
    file_size: int = Field(..., ge=0, description="File size in bytes")
    file_type: str = Field(..., description="File type (pdf, doc, docx)")
    uploaded_at: Optional[date] = Field(None, description="Upload timestamp")
    cloudinary_id: Optional[str] = Field(None, description="Cloudinary public ID")


class CandidateMetadata(BaseDBModel):
    """
    Candidate metadata model
    """
    ip_address: Optional[str] = Field(None, description="IP address of submission")
    user_agent: Optional[str] = Field(None, description="User agent string")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    source: Optional[str] = Field(None, description="Source of registration (website, social media, etc.)")
    device_type: Optional[str] = Field(None, description="Device type (mobile, desktop, tablet)")
    browser: Optional[str] = Field(None, description="Browser name and version")


class Candidate(BaseDBModel):
    """
    Complete candidate model
    """
    personal_details: CandidatePersonalDetails
    professional_details: CandidateProfessionalDetails
    resume: CandidateResume
    consent_accepted: bool = Field(..., description="Whether consent was accepted")
    
    # Status fields
    status: str = Field(default="new", description="Candidate status")
    status_changed_at: Optional[date] = Field(None, description="When status was last changed")
    status_notes: Optional[str] = Field(None, description="Notes about status change")
    
    # Admin fields
    assigned_to: Optional[str] = Field(None, description="Admin user assigned to this candidate")
    priority: Optional[str] = Field(default="medium", description="Priority level")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    
    # Metadata
    metadata: Optional[CandidateMetadata] = Field(None, description="Submission metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "personal_details": {
                    "full_name": "John Doe",
                    "mobile": "9876543210",
                    "whatsapp": "9876543210",
                    "email": "john.doe@example.com",
                    "current_location": "Coimbatore",
                    "preferred_location": "Coimbatore, Chennai"
                },
                "professional_details": {
                    "highest_qualification": "MBA",
                    "specialization": "Human Resources",
                    "total_experience": "5 years",
                    "current_company": "ABC Corporation",
                    "current_designation": "HR Manager",
                    "current_salary": 1200000,
                    "expected_salary": 1500000,
                    "notice_period": "30 days",
                    "skills": ["Recruitment", "Talent Acquisition", "HR Management"],
                    "preferred_job_role": "HR Manager",
                    "industry": "Human Resources"
                },
                "resume": {
                    "url": "https://res.cloudinary.com/.../resume.pdf",
                    "file_name": "John_Doe_Resume.pdf",
                    "file_size": 2048000,
                    "file_type": "pdf"
                },
                "consent_accepted": True,
                "status": "new"
            }
        }


class CandidateCreate(BaseDBModel):
    """
    Model for creating a new candidate (without DB fields)
    """
    personal_details: CandidatePersonalDetails
    professional_details: CandidateProfessionalDetails
    consent_accepted: bool
    
    class Config:
        schema_extra = {
            "example": {
                "personal_details": {
                    "full_name": "John Doe",
                    "mobile": "9876543210",
                    "email": "john.doe@example.com",
                    "current_location": "Coimbatore"
                },
                "professional_details": {
                    "highest_qualification": "MBA",
                    "total_experience": "5 years",
                    "skills": ["Recruitment", "HR Management"]
                },
                "consent_accepted": True
            }
        }


class CandidateUpdate(BaseDBModel):
    """
    Model for updating candidate information
    """
    status: Optional[str] = None
    status_notes: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "contacted",
                "status_notes": "Initial contact made via email",
                "priority": "high"
            }
        }


class CandidateResponse(BaseDBModel):
    """
    Candidate response model for API
    """
    candidate: Candidate
    success: bool = True
    message: Optional[str] = None


class CandidatesListResponse(BaseDBModel):
    """
    List of candidates response model
    """
    candidates: List[Candidate]
    total: int
    page: int = 1
    limit: int = 10
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False
    success: bool = True