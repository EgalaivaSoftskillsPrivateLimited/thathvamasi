"""
Candidate schemas for Thathvamasi HR Consultancy
"""

import re
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, validator, constr
from pydantic.types import conint

from app.schemas.base import PaginationParams


# Base schemas
class CandidateBase(BaseModel):
    """Base schema for candidate"""
    status: Optional[str] = Field("new", description="Candidate status")
    priority: Optional[str] = Field("medium", description="Priority level")
    tags: Optional[List[str]] = Field([], description="Tags for categorization")
    source: Optional[str] = Field(None, description="Source of candidate")
    referrer: Optional[str] = Field(None, description="Referrer information")
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ["new", "contacted", "shortlisted", "rejected", "hired", "on_hold"]
        if v and v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        allowed_priorities = ["low", "medium", "high", "urgent"]
        if v and v not in allowed_priorities:
            raise ValueError(f"Priority must be one of: {allowed_priorities}")
        return v


class CandidatePersonalDetailsBase(BaseModel):
    """Base schema for candidate personal details"""
    full_name: str = Field(..., min_length=2, max_length=255, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    mobile: str = Field(..., min_length=10, max_length=20, description="Mobile number")
    whatsapp: Optional[str] = Field(None, min_length=10, max_length=20, description="WhatsApp number")
    current_location: str = Field(..., min_length=2, max_length=255, description="Current location")
    preferred_location: Optional[str] = Field(None, max_length=255, description="Preferred location")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    marital_status: Optional[str] = Field(None, description="Marital status")
    address: Optional[str] = Field(None, description="Full address")
    city: Optional[str] = Field(None, max_length=100, description="City")
    state: Optional[str] = Field(None, max_length=100, description="State")
    country: str = Field("India", description="Country")
    pincode: Optional[str] = Field(None, max_length=10, description="Pincode")
    emergency_contact_name: Optional[str] = Field(None, max_length=255, description="Emergency contact name")
    emergency_contact_phone: Optional[str] = Field(None, min_length=10, max_length=20, description="Emergency contact phone")
    emergency_contact_relation: Optional[str] = Field(None, max_length=50, description="Emergency contact relation")
    
    @validator('mobile', 'whatsapp', 'emergency_contact_phone')
    def validate_phone_number(cls, v, field):
        if v is None:
            return v
        # Remove any non-digit characters
        cleaned = re.sub(r'\D', '', v)
        if len(cleaned) < 10:
            raise ValueError(f"{field.name} must be at least 10 digits")
        return v
    
    @validator('gender')
    def validate_gender(cls, v):
        if v and v.lower() not in ["male", "female", "other", "prefer not to say"]:
            raise ValueError("Gender must be male, female, other, or prefer not to say")
        return v
    
    @validator('marital_status')
    def validate_marital_status(cls, v):
        if v and v.lower() not in ["single", "married", "divorced", "widowed"]:
            raise ValueError("Marital status must be single, married, divorced, or widowed")
        return v


class CandidateProfessionalDetailsBase(BaseModel):
    """Base schema for candidate professional details"""
    highest_qualification: str = Field(..., max_length=255, description="Highest qualification")
    specialization: Optional[str] = Field(None, max_length=255, description="Specialization")
    university: Optional[str] = Field(None, max_length=255, description="University/College")
    graduation_year: Optional[int] = Field(None, ge=1900, le=2100, description="Graduation year")
    total_experience: str = Field(..., max_length=50, description="Total experience")
    years_of_experience: Optional[float] = Field(None, ge=0, description="Years of experience")
    current_company: Optional[str] = Field(None, max_length=255, description="Current company")
    current_designation: Optional[str] = Field(None, max_length=255, description="Current designation")
    current_salary: Optional[float] = Field(None, ge=0, description="Current annual salary")
    current_salary_currency: str = Field("INR", description="Current salary currency")
    expected_salary: Optional[float] = Field(None, ge=0, description="Expected annual salary")
    expected_salary_currency: str = Field("INR", description="Expected salary currency")
    notice_period: Optional[str] = Field(None, max_length=50, description="Notice period")
    notice_period_days: Optional[int] = Field(None, ge=0, description="Notice period in days")
    skills: List[str] = Field([], description="Skills")
    preferred_job_role: Optional[str] = Field(None, max_length=255, description="Preferred job role")
    preferred_industry: Optional[str] = Field(None, max_length=255, description="Preferred industry")
    job_type_preference: Optional[str] = Field(None, description="Job type preference")
    work_preference: Optional[str] = Field(None, description="Work preference")
    languages_known: List[str] = Field([], description="Languages known")
    certifications: List[str] = Field([], description="Certifications")
    achievements: Optional[str] = Field(None, description="Achievements")
    
    @validator('job_type_preference')
    def validate_job_type(cls, v):
        if v and v.lower() not in ["permanent", "contract", "temporary", "internship"]:
            raise ValueError("Job type must be permanent, contract, temporary, or internship")
        return v
    
    @validator('work_preference')
    def validate_work_preference(cls, v):
        if v and v.lower() not in ["onsite", "remote", "hybrid"]:
            raise ValueError("Work preference must be onsite, remote, or hybrid")
        return v


class CandidateWorkExperienceBase(BaseModel):
    """Base schema for candidate work experience"""
    company_name: str = Field(..., max_length=255, description="Company name")
    company_industry: Optional[str] = Field(None, max_length=255, description="Company industry")
    company_size: Optional[str] = Field(None, max_length=50, description="Company size")
    designation: str = Field(..., max_length=255, description="Designation")
    department: Optional[str] = Field(None, max_length=255, description="Department")
    employment_type: Optional[str] = Field(None, description="Employment type")
    start_date: date = Field(..., description="Start date")
    end_date: Optional[date] = Field(None, description="End date (null for current)")
    is_current: bool = Field(False, description="Is current job")
    location: Optional[str] = Field(None, max_length=255, description="Location")
    work_mode: Optional[str] = Field(None, description="Work mode")
    responsibilities: List[str] = Field([], description="Responsibilities")
    achievements: List[str] = Field([], description="Achievements")
    salary: Optional[float] = Field(None, ge=0, description="Salary")
    salary_currency: str = Field("INR", description="Salary currency")
    reason_for_leaving: Optional[str] = Field(None, description="Reason for leaving")
    references: Optional[Dict[str, Any]] = Field(None, description="References")
    
    @validator('employment_type')
    def validate_employment_type(cls, v):
        if v and v.lower() not in ["full_time", "part_time", "contract", "internship", "freelance"]:
            raise ValueError("Employment type must be full_time, part_time, contract, internship, or freelance")
        return v
    
    @validator('work_mode')
    def validate_work_mode(cls, v):
        if v and v.lower() not in ["onsite", "remote", "hybrid"]:
            raise ValueError("Work mode must be onsite, remote, or hybrid")
        return v
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError("End date must be after start date")
        return v


class CandidateEducationBase(BaseModel):
    """Base schema for candidate education"""
    institution_name: str = Field(..., max_length=255, description="Institution name")
    institution_type: Optional[str] = Field(None, max_length=50, description="Institution type")
    institution_location: Optional[str] = Field(None, max_length=255, description="Institution location")
    qualification: str = Field(..., max_length=255, description="Qualification")
    specialization: Optional[str] = Field(None, max_length=255, description="Specialization")
    degree_type: Optional[str] = Field(None, max_length=50, description="Degree type")
    start_date: Optional[date] = Field(None, description="Start date")
    end_date: Optional[date] = Field(None, description="End date")
    is_completed: bool = Field(True, description="Is completed")
    grade: Optional[str] = Field(None, max_length=20, description="Grade")
    score: Optional[float] = Field(None, description="Score")
    max_score: Optional[float] = Field(None, description="Maximum score")
    description: Optional[str] = Field(None, description="Description")
    achievements: List[str] = Field([], description="Achievements")
    
    @validator('degree_type')
    def validate_degree_type(cls, v):
        if v and v.lower() not in ["bachelors", "masters", "diploma", "phd", "high_school", "certification"]:
            raise ValueError("Degree type must be bachelors, masters, diploma, phd, high_school, or certification")
        return v
    
    @validator('end_date')
    def validate_education_dates(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError("End date must be after start date")
        return v


class CandidateMetadataBase(BaseModel):
    """Base schema for candidate metadata"""
    ip_address: Optional[str] = Field(None, max_length=45, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    device_type: Optional[str] = Field(None, max_length=50, description="Device type")
    browser: Optional[str] = Field(None, max_length=100, description="Browser")
    operating_system: Optional[str] = Field(None, max_length=100, description="Operating system")
    referrer_url: Optional[str] = Field(None, description="Referrer URL")
    landing_page: Optional[str] = Field(None, description="Landing page")
    utm_source: Optional[str] = Field(None, max_length=100, description="UTM source")
    utm_medium: Optional[str] = Field(None, max_length=100, description="UTM medium")
    utm_campaign: Optional[str] = Field(None, max_length=100, description="UTM campaign")
    utm_term: Optional[str] = Field(None, max_length=100, description="UTM term")
    utm_content: Optional[str] = Field(None, max_length=100, description="UTM content")
    form_version: Optional[str] = Field(None, max_length=50, description="Form version")
    form_fields: Optional[Dict[str, Any]] = Field(None, description="Form fields")


# Request schemas
class CandidateCreate(CandidateBase):
    """Schema for creating a new candidate"""
    personal_details: CandidatePersonalDetailsBase
    professional_details: CandidateProfessionalDetailsBase
    work_experiences: Optional[List[CandidateWorkExperienceBase]] = []
    educations: Optional[List[CandidateEducationBase]] = []
    metadata: Optional[CandidateMetadataBase] = None
    consent_accepted: bool = Field(..., description="Whether consent was accepted")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "new",
                "priority": "medium",
                "tags": ["software", "developer"],
                "source": "website",
                "referrer": "Google search",
                "personal_details": {
                    "full_name": "John Doe",
                    "email": "john.doe@example.com",
                    "mobile": "9876543210",
                    "whatsapp": "9876543210",
                    "current_location": "Bengaluru, Karnataka",
                    "preferred_location": "Bengaluru, Hyderabad",
                    "date_of_birth": "1990-01-15",
                    "gender": "male",
                    "marital_status": "single",
                    "address": "123 Main Street",
                    "city": "Bengaluru",
                    "state": "Karnataka",
                    "country": "India",
                    "pincode": "560001",
                    "emergency_contact_name": "Jane Doe",
                    "emergency_contact_phone": "9876543211",
                    "emergency_contact_relation": "Sister"
                },
                "professional_details": {
                    "highest_qualification": "M.Tech",
                    "specialization": "Computer Science",
                    "university": "IIT Delhi",
                    "graduation_year": 2015,
                    "total_experience": "8 years",
                    "years_of_experience": 8.0,
                    "current_company": "Tech Solutions Inc.",
                    "current_designation": "Senior Software Engineer",
                    "current_salary": 1800000.0,
                    "current_salary_currency": "INR",
                    "expected_salary": 2200000.0,
                    "expected_salary_currency": "INR",
                    "notice_period": "30 days",
                    "notice_period_days": 30,
                    "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                    "preferred_job_role": "Backend Developer",
                    "preferred_industry": "Technology",
                    "job_type_preference": "permanent",
                    "work_preference": "hybrid",
                    "languages_known": ["English", "Hindi", "Kannada"],
                    "certifications": ["AWS Certified Developer", "Python Certification"],
                    "achievements": "Developed a microservices architecture that improved performance by 40%"
                },
                "work_experiences": [
                    {
                        "company_name": "Tech Solutions Inc.",
                        "designation": "Senior Software Engineer",
                        "start_date": "2020-01-15",
                        "end_date": None,
                        "is_current": True,
                        "responsibilities": ["API development", "System design", "Team mentoring"],
                        "achievements": ["Reduced API response time by 60%"]
                    }
                ],
                "educations": [
                    {
                        "institution_name": "IIT Delhi",
                        "qualification": "M.Tech",
                        "specialization": "Computer Science",
                        "start_date": "2013-07-01",
                        "end_date": "2015-05-31"
                    }
                ],
                "metadata": {
                    "ip_address": "192.168.1.1",
                    "user_agent": "Mozilla/5.0",
                    "device_type": "desktop",
                    "browser": "Chrome"
                },
                "consent_accepted": True
            }
        }


class CandidateUpdate(CandidateBase):
    """Schema for updating a candidate"""
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    referrer: Optional[str] = None
    assigned_to: Optional[UUID] = None
    status_notes: Optional[str] = None


class CandidatePersonalDetailsUpdate(CandidatePersonalDetailsBase):
    """Schema for updating candidate personal details"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    current_location: Optional[str] = None
    country: Optional[str] = None


class CandidateProfessionalDetailsUpdate(CandidateProfessionalDetailsBase):
    """Schema for updating candidate professional details"""
    highest_qualification: Optional[str] = None
    total_experience: Optional[str] = None
    skills: Optional[List[str]] = None
    languages_known: Optional[List[str]] = None


# Response schemas
class CandidatePersonalDetailsResponse(CandidatePersonalDetailsBase):
    """Response schema for candidate personal details"""
    id: UUID
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class CandidateProfessionalDetailsResponse(CandidateProfessionalDetailsBase):
    """Response schema for candidate professional details"""
    id: UUID
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class CandidateWorkExperienceResponse(CandidateWorkExperienceBase):
    """Response schema for candidate work experience"""
    id: UUID
    professional_details_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class CandidateEducationResponse(CandidateEducationBase):
    """Response schema for candidate education"""
    id: UUID
    professional_details_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class CandidateMetadataResponse(CandidateMetadataBase):
    """Response schema for candidate metadata"""
    id: UUID
    candidate_id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True


class CandidateResumeResponse(BaseModel):
    """Response schema for candidate resume"""
    id: UUID
    candidate_id: UUID
    file_url: str
    file_name: str
    file_size: int
    file_type: str
    cloudinary_id: Optional[str]
    version: int
    is_primary: bool
    uploaded_at: datetime
    uploaded_by: Optional[str]
    is_parsed: bool
    parsed_data: Optional[Dict[str, Any]]
    
    class Config:
        orm_mode = True


class CandidateNoteResponse(BaseModel):
    """Response schema for candidate note"""
    id: UUID
    candidate_id: UUID
    title: Optional[str]
    content: str
    note_type: str
    created_by: Optional[UUID]
    created_by_name: Optional[str]
    is_private: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class CandidateInterviewResponse(BaseModel):
    """Response schema for candidate interview"""
    id: UUID
    candidate_id: UUID
    interview_type: str
    interview_stage: str
    scheduled_at: datetime
    duration_minutes: int
    timezone: str
    interviewer_ids: List[UUID]
    interviewer_names: List[str]
    meeting_link: Optional[str]
    meeting_platform: Optional[str]
    location: Optional[str]
    status: str
    feedback: Optional[str]
    rating: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class CandidateResponse(CandidateBase):
    """Response schema for candidate"""
    id: UUID
    assigned_to: Optional[UUID]
    consent_accepted: bool
    consent_accepted_at: Optional[datetime]
    status_changed_at: Optional[datetime]
    status_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    personal_details: Optional[CandidatePersonalDetailsResponse]
    professional_details: Optional[CandidateProfessionalDetailsResponse]
    resumes: List[CandidateResumeResponse] = []
    metadata: Optional[CandidateMetadataResponse]
    notes: List[CandidateNoteResponse] = []
    interviews: List[CandidateInterviewResponse] = []
    
    class Config:
        orm_mode = True


class CandidateDetailResponse(CandidateResponse):
    """Detailed response schema for candidate with nested data"""
    professional_details_with_experience: Optional[CandidateProfessionalDetailsResponse] = None
    work_experiences: List[CandidateWorkExperienceResponse] = []
    educations: List[CandidateEducationResponse] = []


# List schemas
class CandidateListResponse(BaseModel):
    """Response schema for candidate list"""
    items: List[CandidateResponse]
    total: int
    page: int
    size: int
    total_pages: int


# Filter schemas
class CandidateFilterParams(BaseModel):
    """Schema for filtering candidates"""
    status: Optional[str] = None
    priority: Optional[str] = None
    source: Optional[str] = None
    location: Optional[str] = None
    min_experience: Optional[float] = None
    max_experience: Optional[float] = None
    skills: Optional[List[str]] = None
    assigned_to: Optional[UUID] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    search: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "new",
                "priority": "high",
                "location": "Bengaluru",
                "skills": ["Python", "FastAPI"],
                "min_experience": 3.0,
                "date_from": "2024-01-01"
            }
        }