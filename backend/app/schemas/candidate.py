"""
Candidate schemas for Thathvamasi HR Consultancy
Pydantic v2 Compatible
"""

import re
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import (
    BaseModel, Field, EmailStr, field_validator, ValidationInfo,
    ConfigDict, model_validator, AliasChoices
)

from app.schemas.base import PaginationParams


# Base schemas
class CandidateBase(BaseModel):
    """Base schema for candidate"""
    status: Optional[str] = Field("new", description="Candidate status")
    priority: Optional[str] = Field("medium", description="Priority level")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")
    source: Optional[str] = Field("website", description="Source of candidate")
    referrer: Optional[str] = Field(None, description="Referrer information")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed_statuses = ["new", "contacted", "shortlisted", "rejected", "hired", "on_hold"]
        if v and v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v
    
    @field_validator('priority')
    @classmethod
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
    whatsapp: Optional[str] = Field(None, max_length=20, description="WhatsApp number")
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
    emergency_contact_phone: Optional[str] = Field(None, max_length=20, description="Emergency contact phone")
    emergency_contact_relation: Optional[str] = Field(None, max_length=50, description="Emergency contact relation")
    
    @field_validator('mobile', 'whatsapp', 'emergency_contact_phone')
    @classmethod
    def validate_phone_number(cls, v, info: ValidationInfo):
        if v is None:
            return v
        cleaned = re.sub(r'\D', '', str(v))
        if len(cleaned) < 10:
            raise ValueError(f"{info.field_name} must be at least 10 digits")
        return cleaned
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v and v.lower() not in ["male", "female", "other", "prefer not to say"]:
            raise ValueError("Gender must be male, female, other, or prefer not to say")
        return v
    
    @field_validator('marital_status')
    @classmethod
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
    skills: List[str] = Field(default_factory=list, description="Skills")
    preferred_job_role: Optional[str] = Field(None, max_length=255, description="Preferred job role")
    preferred_industry: Optional[str] = Field(None, max_length=255, description="Preferred industry")
    job_type_preference: Optional[str] = Field(None, description="Job type preference")
    work_preference: Optional[str] = Field(None, description="Work preference")
    languages_known: List[str] = Field(default_factory=list, description="Languages known")
    certifications: List[str] = Field(default_factory=list, description="Certifications")
    achievements: Optional[str] = Field(None, description="Achievements")
    
    @field_validator('job_type_preference')
    @classmethod
    def validate_job_type(cls, v):
        if v and v.lower() not in ["permanent", "contract", "temporary", "internship"]:
            raise ValueError("Job type must be permanent, contract, temporary, or internship")
        return v
    
    @field_validator('work_preference')
    @classmethod
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
    responsibilities: List[str] = Field(default_factory=list, description="Responsibilities")
    achievements: List[str] = Field(default_factory=list, description="Achievements")
    salary: Optional[float] = Field(None, ge=0, description="Salary")
    salary_currency: str = Field("INR", description="Salary currency")
    reason_for_leaving: Optional[str] = Field(None, description="Reason for leaving")
    references: Optional[Dict[str, Any]] = Field(None, description="References")
    
    @field_validator('employment_type')
    @classmethod
    def validate_employment_type(cls, v):
        if v and v.lower() not in ["full_time", "part_time", "contract", "internship", "freelance"]:
            raise ValueError("Employment type must be full_time, part_time, contract, internship, or freelance")
        return v
    
    @field_validator('work_mode')
    @classmethod
    def validate_work_mode(cls, v):
        if v and v.lower() not in ["onsite", "remote", "hybrid"]:
            raise ValueError("Work mode must be onsite, remote, or hybrid")
        return v
    
    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v, info: ValidationInfo):
        start_date = info.data.get('start_date') if info.data else None
        if v and start_date and v < start_date:
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
    achievements: List[str] = Field(default_factory=list, description="Achievements")
    
    @field_validator('degree_type')
    @classmethod
    def validate_degree_type(cls, v):
        if v and v.lower() not in ["bachelors", "masters", "diploma", "phd", "high_school", "certification"]:
            raise ValueError("Degree type must be bachelors, masters, diploma, phd, high_school, or certification")
        return v
    
    @field_validator('end_date')
    @classmethod
    def validate_education_dates(cls, v, info: ValidationInfo):
        start_date = info.data.get('start_date') if info.data else None
        if v and start_date and v < start_date:
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
    """
    Schema for creating a new candidate.
    Supports both nested structure and flat form payloads.
    """
    personal_details: CandidatePersonalDetailsBase
    professional_details: CandidateProfessionalDetailsBase
    work_experiences: Optional[List[CandidateWorkExperienceBase]] = Field(default_factory=list)
    educations: Optional[List[CandidateEducationBase]] = Field(default_factory=list)
    metadata: Optional[CandidateMetadataBase] = None
    consent_accepted: bool = Field(True, description="Whether consent was accepted")

    @model_validator(mode='before')
    @classmethod
    def handle_flat_payload(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # If flat fields are passed at root without personal_details/professional_details
            if "personal_details" not in data and ("name" in data or "full_name" in data):
                name = data.get("full_name") or data.get("name", "Unknown Candidate")
                email = data.get("email", "")
                mobile = data.get("mobile", "")
                current_location = data.get("current_location") or data.get("currentLocation", "Coimbatore")
                whatsapp = data.get("whatsapp") or mobile
                pref_location = data.get("preferred_location") or data.get("preferredLocation")

                data["personal_details"] = {
                    "full_name": name,
                    "email": email,
                    "mobile": mobile,
                    "whatsapp": whatsapp,
                    "current_location": current_location,
                    "preferred_location": pref_location,
                    "country": "India"
                }

            if "professional_details" not in data and ("qualification" in data or "highest_qualification" in data or "skills" in data):
                qual = data.get("highest_qualification") or data.get("qualification", "Graduate")
                exp = data.get("total_experience") or data.get("experience", "1-3 Years")
                raw_skills = data.get("skills", [])
                if isinstance(raw_skills, str):
                    raw_skills = [s.strip() for s in raw_skills.split(",") if s.strip()]

                data["professional_details"] = {
                    "highest_qualification": qual,
                    "total_experience": str(exp),
                    "current_company": data.get("current_company") or data.get("currentCompany"),
                    "current_designation": data.get("current_designation") or data.get("currentDesignation"),
                    "notice_period": data.get("notice_period") or data.get("noticePeriod", "Immediate"),
                    "skills": raw_skills
                }

            if "consent_accepted" not in data:
                data["consent_accepted"] = True

        return data

    model_config = ConfigDict(
        json_schema_extra={
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
                    "languages_known": ["English", "Hindi"],
                    "certifications": ["AWS Certified Developer"],
                    "achievements": "Developed microservices architecture"
                },
                "work_experiences": [],
                "educations": [],
                "consent_accepted": True
            }
        }
    )


class CandidateUpdate(CandidateBase):
    """Schema for updating a candidate"""
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    referrer: Optional[str] = None
    assigned_to: Optional[UUID] = None
    status_notes: Optional[str] = None


class CandidatePersonalDetailsUpdate(BaseModel):
    """Schema for updating candidate personal details"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    whatsapp: Optional[str] = None
    current_location: Optional[str] = None
    preferred_location: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None


class CandidateProfessionalDetailsUpdate(BaseModel):
    """Schema for updating candidate professional details"""
    highest_qualification: Optional[str] = None
    specialization: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    total_experience: Optional[str] = None
    years_of_experience: Optional[float] = None
    current_company: Optional[str] = None
    current_designation: Optional[str] = None
    current_salary: Optional[float] = None
    current_salary_currency: Optional[str] = None
    expected_salary: Optional[float] = None
    expected_salary_currency: Optional[str] = None
    notice_period: Optional[str] = None
    notice_period_days: Optional[int] = None
    skills: Optional[List[str]] = None
    preferred_job_role: Optional[str] = None
    preferred_industry: Optional[str] = None
    job_type_preference: Optional[str] = None
    work_preference: Optional[str] = None
    languages_known: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    achievements: Optional[str] = None


# Response schemas
class CandidatePersonalDetailsResponse(CandidatePersonalDetailsBase):
    """Response schema for candidate personal details"""
    id: UUID
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CandidateProfessionalDetailsResponse(CandidateProfessionalDetailsBase):
    """Response schema for candidate professional details"""
    id: UUID
    candidate_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CandidateWorkExperienceResponse(CandidateWorkExperienceBase):
    """Response schema for candidate work experience"""
    id: UUID
    professional_details_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CandidateEducationResponse(CandidateEducationBase):
    """Response schema for candidate education"""
    id: UUID
    professional_details_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CandidateMetadataResponse(CandidateMetadataBase):
    """Response schema for candidate metadata"""
    id: UUID
    candidate_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CandidateResumeResponse(BaseModel):
    """Response schema for candidate resume"""
    id: UUID
    candidate_id: UUID
    file_url: str
    file_name: str
    file_size: int
    file_type: str
    cloudinary_id: Optional[str] = None
    version: int = 1
    is_primary: bool = True
    uploaded_at: datetime
    uploaded_by: Optional[str] = None
    is_parsed: bool = False
    parsed_data: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)


class CandidateNoteResponse(BaseModel):
    """Response schema for candidate note"""
    id: UUID
    candidate_id: UUID
    title: Optional[str] = None
    content: str
    note_type: str = "general"
    created_by: Optional[UUID] = None
    created_by_name: Optional[str] = None
    is_private: bool = False
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CandidateInterviewResponse(BaseModel):
    """Response schema for candidate interview"""
    id: UUID
    candidate_id: UUID
    interview_type: str
    interview_stage: str
    scheduled_at: datetime
    duration_minutes: int
    timezone: str = "IST"
    interviewer_ids: List[UUID] = Field(default_factory=list)
    interviewer_names: List[str] = Field(default_factory=list)
    meeting_link: Optional[str] = None
    meeting_platform: Optional[str] = None
    location: Optional[str] = None
    status: str = "scheduled"
    feedback: Optional[str] = None
    rating: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CandidateResponse(CandidateBase):
    """Response schema for candidate"""
    id: UUID
    assigned_to: Optional[UUID] = None
    consent_accepted: bool = True
    consent_accepted_at: Optional[datetime] = None
    status_changed_at: Optional[datetime] = None
    status_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    personal_details: Optional[CandidatePersonalDetailsResponse] = None
    professional_details: Optional[CandidateProfessionalDetailsResponse] = None
    resumes: List[CandidateResumeResponse] = Field(default_factory=list)
    metadata: Optional[CandidateMetadataResponse] = Field(
        default=None,
        validation_alias=AliasChoices('candidate_metadata', 'metadata'),
        serialization_alias='metadata'
    )
    notes: List[CandidateNoteResponse] = Field(default_factory=list)
    interviews: List[CandidateInterviewResponse] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)


class CandidateDetailResponse(CandidateResponse):
    """Detailed response schema for candidate with nested data"""
    professional_details_with_experience: Optional[CandidateProfessionalDetailsResponse] = None
    work_experiences: List[CandidateWorkExperienceResponse] = Field(default_factory=list)
    educations: List[CandidateEducationResponse] = Field(default_factory=list)


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
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "new",
                "priority": "high",
                "location": "Bengaluru",
                "skills": ["Python", "FastAPI"],
                "min_experience": 3.0,
                "date_from": "2024-01-01"
            }
        }
    )