"""
SQLAlchemy Candidate models for Thathvamasi HR Consultancy
"""

import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, Integer, Float, ForeignKey, Text, ARRAY, Index, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Candidate(Base):
    """
    Main candidate model
    """
    __tablename__ = "candidates"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Status fields
    status = Column(String(50), default="new", nullable=False)  # new, contacted, shortlisted, rejected, hired
    status_changed_at = Column(DateTime(timezone=True), nullable=True)
    status_notes = Column(Text, nullable=True)
    
    # Assignment
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, urgent
    tags = Column(ARRAY(String), default=[], nullable=False)
    
    # Consent
    consent_accepted = Column(Boolean, default=False, nullable=False)
    consent_accepted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Source tracking
    source = Column(String(100), nullable=True)  # website, referral, social_media, etc.
    referrer = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    personal_details = relationship("CandidatePersonalDetails", uselist=False, back_populates="candidate", cascade="all, delete-orphan")
    professional_details = relationship("CandidateProfessionalDetails", uselist=False, back_populates="candidate", cascade="all, delete-orphan")
    resumes = relationship("CandidateResume", back_populates="candidate", cascade="all, delete-orphan")
    candidate_metadata = relationship("CandidateMetadata", uselist=False, back_populates="candidate", cascade="all, delete-orphan")
    notes = relationship("CandidateNote", back_populates="candidate", cascade="all, delete-orphan")
    interviews = relationship("CandidateInterview", back_populates="candidate", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_candidates_status', 'status'),
        Index('ix_candidates_created_at', 'created_at'),
        Index('ix_candidates_assigned_to', 'assigned_to'),
        Index('ix_candidates_priority', 'priority'),
        Index('ix_candidates_source', 'source'),
    )
    
    def __repr__(self):
        return f"<Candidate(id={self.id}, status={self.status})>"


class CandidatePersonalDetails(Base):
    """
    Candidate personal details
    """
    __tablename__ = "candidate_personal_details"
    
    # Primary key and foreign key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Personal information
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(20), nullable=False)
    whatsapp = Column(String(20), nullable=True)
    
    # Location
    current_location = Column(String(255), nullable=False)
    preferred_location = Column(String(255), nullable=True)
    
    # Demographic information (optional)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)
    marital_status = Column(String(20), nullable=True)
    
    # Address
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="India", nullable=False)
    pincode = Column(String(10), nullable=True)
    
    # Emergency contact
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relation = Column(String(50), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="personal_details")
    
    # Indexes
    __table_args__ = (
        Index('ix_candidate_personal_details_email', 'email'),
        Index('ix_candidate_personal_details_mobile', 'mobile'),
        Index('ix_candidate_personal_details_location', 'current_location'),
    )
    
    def __repr__(self):
        return f"<CandidatePersonalDetails(id={self.id}, candidate_id={self.candidate_id}, name={self.full_name})>"


class CandidateProfessionalDetails(Base):
    """
    Candidate professional details
    """
    __tablename__ = "candidate_professional_details"
    
    # Primary key and foreign key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Education
    highest_qualification = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=True)
    university = Column(String(255), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    
    # Experience
    total_experience = Column(String(50), nullable=False)  # e.g., "5 years", "2 months"
    years_of_experience = Column(Float, nullable=True)
    
    # Current employment
    current_company = Column(String(255), nullable=True)
    current_designation = Column(String(255), nullable=True)
    current_salary = Column(Numeric(12, 2), nullable=True)  # Annual CTC in INR, 12 digits with 2 decimal places
    current_salary_currency = Column(String(10), default="INR", nullable=False)
    
    # Expected
    expected_salary = Column(Numeric(12, 2), nullable=True)  # Annual CTC in INR, 12 digits with 2 decimal places
    expected_salary_currency = Column(String(10), default="INR", nullable=False)
    
    # Notice period
    notice_period = Column(String(50), nullable=True)  # e.g., "15 days", "1 month", "Immediate"
    notice_period_days = Column(Integer, nullable=True)
    
    # Skills and preferences
    skills = Column(ARRAY(String), default=[], nullable=False)
    preferred_job_role = Column(String(255), nullable=True)
    preferred_industry = Column(String(255), nullable=True)
    job_type_preference = Column(String(50), nullable=True)  # permanent, contract, temporary, internship
    work_preference = Column(String(50), nullable=True)  # onsite, remote, hybrid
    
    # Languages
    languages_known = Column(ARRAY(String), default=[], nullable=False)
    
    # Additional information
    certifications = Column(ARRAY(String), default=[], nullable=False)
    achievements = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="professional_details")
    work_experiences = relationship("CandidateWorkExperience", back_populates="professional_details", cascade="all, delete-orphan")
    educations = relationship("CandidateEducation", back_populates="professional_details", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_candidate_professional_details_skills', 'skills', postgresql_using='gin'),
        Index('ix_candidate_professional_details_experience', 'years_of_experience'),
        Index('ix_candidate_professional_details_qualification', 'highest_qualification'),
    )
    
    def __repr__(self):
        return f"<CandidateProfessionalDetails(id={self.id}, candidate_id={self.candidate_id})>"


class CandidateResume(Base):
    """
    Candidate resume files
    """
    __tablename__ = "candidate_resumes"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    
    # File information
    file_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_type = Column(String(50), nullable=False)  # pdf, doc, docx
    cloudinary_id = Column(String(255), nullable=True)
    
    # Version tracking
    version = Column(Integer, default=1, nullable=False)
    is_primary = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    uploaded_by = Column(String(255), nullable=True)  # candidate or admin
    
    # Parsing information (if resume is parsed)
    is_parsed = Column(Boolean, default=False, nullable=False)
    parsed_data = Column(JSONB, nullable=True)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="resumes")
    
    # Indexes
    __table_args__ = (
        Index('ix_candidate_resumes_candidate_id', 'candidate_id'),
        Index('ix_candidate_resumes_is_primary', 'is_primary'),
        Index('ix_candidate_resumes_uploaded_at', 'uploaded_at'),
    )
    
    def __repr__(self):
        return f"<CandidateResume(id={self.id}, candidate_id={self.candidate_id}, file={self.file_name})>"


class CandidateMetadata(Base):
    """
    Candidate submission metadata
    """
    __tablename__ = "candidate_metadata"
    
    # Primary key and foreign key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Technical metadata
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    device_type = Column(String(50), nullable=True)  # mobile, desktop, tablet
    browser = Column(String(100), nullable=True)
    operating_system = Column(String(100), nullable=True)
    
    # Referral data
    referrer_url = Column(Text, nullable=True)
    landing_page = Column(Text, nullable=True)
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    utm_term = Column(String(100), nullable=True)
    utm_content = Column(String(100), nullable=True)
    
    # Form data
    form_version = Column(String(50), nullable=True)
    form_fields = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="candidate_metadata")
    
    def __repr__(self):
        return f"<CandidateMetadata(id={self.id}, candidate_id={self.candidate_id})>"


class CandidateWorkExperience(Base):
    """
    Candidate work experience details
    """
    __tablename__ = "candidate_work_experiences"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    professional_details_id = Column(UUID(as_uuid=True), ForeignKey("candidate_professional_details.id", ondelete="CASCADE"), nullable=False)
    
    # Company information
    company_name = Column(String(255), nullable=False)
    company_industry = Column(String(255), nullable=True)
    company_size = Column(String(50), nullable=True)
    
    # Position details
    designation = Column(String(255), nullable=False)
    department = Column(String(255), nullable=True)
    employment_type = Column(String(50), nullable=True)  # full_time, part_time, contract, internship
    
    # Dates
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # null means current job
    is_current = Column(Boolean, default=False, nullable=False)
    
    # Location
    location = Column(String(255), nullable=True)
    work_mode = Column(String(50), nullable=True)  # onsite, remote, hybrid
    
    # Responsibilities and achievements
    responsibilities = Column(ARRAY(String), default=[], nullable=False)
    achievements = Column(ARRAY(String), default=[], nullable=False)
    
    # Salary
    salary = Column(Float, nullable=True)
    salary_currency = Column(String(10), default="INR", nullable=False)
    
    # Reason for leaving
    reason_for_leaving = Column(Text, nullable=True)
    
    # References
    references = Column(JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    professional_details = relationship("CandidateProfessionalDetails", back_populates="work_experiences")
    
    # Indexes
    __table_args__ = (
        Index('ix_candidate_work_experiences_company', 'company_name'),
        Index('ix_candidate_work_experiences_designation', 'designation'),
        Index('ix_candidate_work_experiences_dates', 'start_date', 'end_date'),
    )
    
    def __repr__(self):
        return f"<CandidateWorkExperience(id={self.id}, company={self.company_name}, designation={self.designation})>"


class CandidateEducation(Base):
    """
    Candidate education details
    """
    __tablename__ = "candidate_educations"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    professional_details_id = Column(UUID(as_uuid=True), ForeignKey("candidate_professional_details.id", ondelete="CASCADE"), nullable=False)
    
    # Institution
    institution_name = Column(String(255), nullable=False)
    institution_type = Column(String(50), nullable=True)  # university, college, school
    institution_location = Column(String(255), nullable=True)
    
    # Qualification
    qualification = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=True)
    degree_type = Column(String(50), nullable=True)  # bachelors, masters, diploma, phd
    
    # Dates
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=True, nullable=False)
    
    # Grades and scores
    grade = Column(String(20), nullable=True)  # CGPA, percentage, grade
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)  # e.g., 10 for CGPA, 100 for percentage
    
    # Additional information
    description = Column(Text, nullable=True)
    achievements = Column(ARRAY(String), default=[], nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    professional_details = relationship("CandidateProfessionalDetails", back_populates="educations")
    
    # Indexes
    __table_args__ = (
        Index('ix_candidate_educations_institution', 'institution_name'),
        Index('ix_candidate_educations_qualification', 'qualification'),
    )
    
    def __repr__(self):
        return f"<CandidateEducation(id={self.id}, institution={self.institution_name}, qualification={self.qualification})>"


class CandidateNote(Base):
    """
    Notes and comments on candidates
    """
    __tablename__ = "candidate_notes"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    
    # Note details
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    note_type = Column(String(50), default="general", nullable=False)  # general, feedback, interview, follow_up
    
    # Author
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by_name = Column(String(255), nullable=True)
    
    # Privacy
    is_private = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="notes")
    
    # Indexes
    __table_args__ = (
        Index('ix_candidate_notes_candidate_id', 'candidate_id'),
        Index('ix_candidate_notes_created_at', 'created_at'),
        Index('ix_candidate_notes_note_type', 'note_type'),
    )
    
    def __repr__(self):
        return f"<CandidateNote(id={self.id}, candidate_id={self.candidate_id}, type={self.note_type})>"


class CandidateInterview(Base):
    """
    Candidate interview scheduling and tracking
    """
    __tablename__ = "candidate_interviews"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    
    # Interview details
    interview_type = Column(String(50), nullable=False)  # phone, video, in_person, technical, hr
    interview_stage = Column(String(50), nullable=False)  # initial, technical, final, hr
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=60, nullable=False)
    timezone = Column(String(50), default="Asia/Kolkata", nullable=False)
    
    # Participants
    interviewer_ids = Column(ARRAY(UUID(as_uuid=True)), default=[], nullable=False)
    interviewer_names = Column(ARRAY(String), default=[], nullable=False)
    
    # Meeting details
    meeting_link = Column(String(500), nullable=True)
    meeting_platform = Column(String(50), nullable=True)  # zoom, google_meet, teams, etc.
    location = Column(String(500), nullable=True)
    
    # Status
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, completed, cancelled, rescheduled
    feedback = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 scale
    
    # Rescheduling
    rescheduled_from = Column(UUID(as_uuid=True), ForeignKey("candidate_interviews.id"), nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="interviews")
    
    # Indexes
    __table_args__ = (
        Index('ix_candidate_interviews_candidate_id', 'candidate_id'),
        Index('ix_candidate_interviews_scheduled_at', 'scheduled_at'),
        Index('ix_candidate_interviews_status', 'status'),
        Index('ix_candidate_interviews_interview_stage', 'interview_stage'),
    )
    
    def __repr__(self):
        return f"<CandidateInterview(id={self.id}, candidate_id={self.candidate_id}, scheduled_at={self.scheduled_at})>"