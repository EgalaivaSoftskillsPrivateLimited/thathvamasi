"""
SQLAlchemy Client/Employer models for Thathvamasi HR Consultancy
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text, ARRAY, Float, Date, UniqueConstraint, Index, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Client(Base):
    """
    Client/Employer model
    """
    __tablename__ = "clients"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company information
    company_name = Column(String(255), nullable=False)
    company_email = Column(String(255), nullable=False)
    company_phone = Column(String(20), nullable=True)
    company_website = Column(String(500), nullable=True)
    
    # Contact person
    contact_person_name = Column(String(255), nullable=False)
    contact_person_email = Column(String(255), nullable=False)
    contact_person_phone = Column(String(20), nullable=False)
    contact_person_designation = Column(String(100), nullable=True)
    
    # Company details
    company_size = Column(String(50), nullable=True)  # 1-50, 51-200, 201-500, 500+
    company_type = Column(String(50), nullable=True)  # private, public, mnc, startup, government
    industry = Column(String(255), nullable=True)
    headquarters = Column(String(255), nullable=True)
    
    # Location
    company_address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="India", nullable=False)
    pincode = Column(String(10), nullable=True)
    
    # Status
    status = Column(String(50), default="new", nullable=False)  # new, contacted, active, inactive, blocked
    status_changed_at = Column(DateTime(timezone=True), nullable=True)
    status_notes = Column(Text, nullable=True)
    
    # Assignment
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    account_manager = Column(String(255), nullable=True)
    
    # Classification
    client_type = Column(String(50), default="regular", nullable=False)  # regular, premium, enterprise
    tags = Column(ARRAY(String), default=[], nullable=False)
    
    # Billing information (optional)
    billing_name = Column(String(255), nullable=True)
    billing_email = Column(String(255), nullable=True)
    billing_phone = Column(String(20), nullable=True)
    billing_address = Column(Text, nullable=True)
    gst_number = Column(String(50), nullable=True)
    pan_number = Column(String(50), nullable=True)
    
    # Source tracking
    source = Column(String(100), nullable=True)  # website, referral, event, cold_call, etc.
    referrer = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    hiring_requirements = relationship("HiringRequirement", back_populates="client", cascade="all, delete-orphan")
    contacts = relationship("ClientContact", back_populates="client", cascade="all, delete-orphan")
    documents = relationship("ClientDocument", back_populates="client", cascade="all, delete-orphan")
    client_metadata = relationship("ClientMetadata", uselist=False, back_populates="client", cascade="all, delete-orphan")
    notes = relationship("ClientNote", back_populates="client", cascade="all, delete-orphan")
    meetings = relationship("ClientMeeting", back_populates="client", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_clients_company_name', 'company_name'),
        Index('ix_clients_company_email', 'company_email'),
        Index('ix_clients_status', 'status'),
        Index('ix_clients_client_type', 'client_type'),
        Index('ix_clients_created_at', 'created_at'),
        Index('ix_clients_assigned_to', 'assigned_to'),
    )
    
    def __repr__(self):
        return f"<Client(id={self.id}, company={self.company_name}, status={self.status})>"


class HiringRequirement(Base):
    """
    Client hiring requirements
    """
    __tablename__ = "hiring_requirements"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    
    # Position details
    position_title = Column(String(255), nullable=False)
    number_of_vacancies = Column(Integer, default=1, nullable=False)
    job_location = Column(String(255), nullable=False)
    
    # Requirements
    required_experience = Column(String(100), nullable=True)  # e.g., "2-5 years"
    required_qualification = Column(String(255), nullable=True)
    key_skills = Column(ARRAY(String), default=[], nullable=False)
    
    # Compensation
    salary_range_min = Column(Numeric(12, 2), nullable=True)  # 12 digits with 2 decimal places
    salary_range_max = Column(Numeric(12, 2), nullable=True)  # 12 digits with 2 decimal places
    salary_currency = Column(String(10), default="INR", nullable=False)
    salary_type = Column(String(50), nullable=True)  # annual, monthly, hourly
    
    # Employment details
    employment_type = Column(String(50), default="permanent", nullable=False)  # permanent, contract, temporary, internship
    work_mode = Column(String(50), nullable=True)  # onsite, remote, hybrid
    shift_timing = Column(String(100), nullable=True)
    
    # Timeline
    expected_joining_timeline = Column(String(100), nullable=True)  # immediate, 15 days, 1 month, etc.
    deadline = Column(Date, nullable=True)
    
    # Job description
    job_description = Column(Text, nullable=True)
    additional_requirements = Column(Text, nullable=True)
    
    # Status
    status = Column(String(50), default="open", nullable=False)  # open, in_progress, filled, cancelled, on_hold
    status_changed_at = Column(DateTime(timezone=True), nullable=True)
    status_notes = Column(Text, nullable=True)
    
    # Priority
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, urgent
    
    # Assignment
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="hiring_requirements")
    jd_documents = relationship("JobDescriptionDocument", back_populates="hiring_requirement", cascade="all, delete-orphan")
    candidates = relationship("HiringRequirementCandidate", back_populates="hiring_requirement", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_hiring_requirements_client_id', 'client_id'),
        Index('ix_hiring_requirements_status', 'status'),
        Index('ix_hiring_requirements_position_title', 'position_title'),
        Index('ix_hiring_requirements_priority', 'priority'),
        Index('ix_hiring_requirements_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<HiringRequirement(id={self.id}, client_id={self.client_id}, position={self.position_title})>"


class JobDescriptionDocument(Base):
    """
    Job description documents
    """
    __tablename__ = "job_description_documents"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hiring_requirement_id = Column(UUID(as_uuid=True), ForeignKey("hiring_requirements.id", ondelete="CASCADE"), nullable=False)
    
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
    uploaded_by = Column(String(255), nullable=True)
    
    # Parsing information (if JD is parsed)
    is_parsed = Column(Boolean, default=False, nullable=False)
    parsed_data = Column(JSONB, nullable=True)
    
    # Relationships
    hiring_requirement = relationship("HiringRequirement", back_populates="jd_documents")
    
    # Indexes
    __table_args__ = (
        Index('ix_job_description_documents_hiring_requirement_id', 'hiring_requirement_id'),
        Index('ix_job_description_documents_is_primary', 'is_primary'),
    )
    
    def __repr__(self):
        return f"<JobDescriptionDocument(id={self.id}, hiring_requirement_id={self.hiring_requirement_id}, file={self.file_name})>"


class ClientContact(Base):
    """
    Additional client contacts
    """
    __tablename__ = "client_contacts"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    
    # Contact information
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    whatsapp = Column(String(20), nullable=True)
    
    # Details
    designation = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)
    is_decision_maker = Column(Boolean, default=False, nullable=False)
    
    # Preferences
    preferred_contact_method = Column(String(50), default="email", nullable=False)  # email, phone, whatsapp
    contact_timing = Column(String(100), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="contacts")
    
    # Indexes
    __table_args__ = (
        Index('ix_client_contacts_client_id', 'client_id'),
        Index('ix_client_contacts_is_primary', 'is_primary'),
        Index('ix_client_contacts_name', 'name'),
    )
    
    def __repr__(self):
        return f"<ClientContact(id={self.id}, client_id={self.client_id}, name={self.name})>"


class ClientDocument(Base):
    """
    Client documents (agreements, proposals, etc.)
    """
    __tablename__ = "client_documents"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    
    # Document information
    document_type = Column(String(100), nullable=False)  # agreement, proposal, invoice, other
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # File information
    file_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)
    cloudinary_id = Column(String(255), nullable=True)
    
    # Status
    status = Column(String(50), default="draft", nullable=False)  # draft, sent, signed, expired, cancelled
    version = Column(Integer, default=1, nullable=False)
    
    # Dates
    issue_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    signed_date = Column(Date, nullable=True)
    
    # Metadata
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    client = relationship("Client", back_populates="documents")
    
    # Indexes
    __table_args__ = (
        Index('ix_client_documents_client_id', 'client_id'),
        Index('ix_client_documents_document_type', 'document_type'),
        Index('ix_client_documents_status', 'status'),
    )
    
    def __repr__(self):
        return f"<ClientDocument(id={self.id}, client_id={self.client_id}, type={self.document_type})>"


class ClientMetadata(Base):
    """
    Client submission metadata
    """
    __tablename__ = "client_metadata"
    
    # Primary key and foreign key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Technical metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    device_type = Column(String(50), nullable=True)
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
    client = relationship("Client", back_populates="client_metadata")
    
    def __repr__(self):
        return f"<ClientMetadata(id={self.id}, client_id={self.client_id})>"


class ClientNote(Base):
    """
    Notes and comments on clients
    """
    __tablename__ = "client_notes"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    
    # Note details
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    note_type = Column(String(50), default="general", nullable=False)  # general, feedback, meeting, follow_up
    
    # Author
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by_name = Column(String(255), nullable=True)
    
    # Privacy
    is_private = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="notes")
    
    # Indexes
    __table_args__ = (
        Index('ix_client_notes_client_id', 'client_id'),
        Index('ix_client_notes_created_at', 'created_at'),
        Index('ix_client_notes_note_type', 'note_type'),
    )
    
    def __repr__(self):
        return f"<ClientNote(id={self.id}, client_id={self.client_id}, type={self.note_type})>"


class ClientMeeting(Base):
    """
    Client meeting scheduling and tracking
    """
    __tablename__ = "client_meetings"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    
    # Meeting details
    meeting_type = Column(String(50), nullable=False)  # discovery, proposal, review, follow_up
    purpose = Column(Text, nullable=True)
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=60, nullable=False)
    timezone = Column(String(50), default="Asia/Kolkata", nullable=False)
    
    # Participants
    host_ids = Column(ARRAY(UUID(as_uuid=True)), default=[], nullable=False)
    host_names = Column(ARRAY(String), default=[], nullable=False)
    client_participants = Column(ARRAY(String), default=[], nullable=False)
    
    # Meeting details
    meeting_link = Column(String(500), nullable=True)
    meeting_platform = Column(String(50), nullable=True)
    location = Column(String(500), nullable=True)
    
    # Agenda and minutes
    agenda = Column(Text, nullable=True)
    minutes = Column(Text, nullable=True)
    decisions = Column(ARRAY(String), default=[], nullable=False)
    action_items = Column(JSONB, nullable=True)
    
    # Status
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, completed, cancelled, rescheduled
    feedback = Column(Text, nullable=True)
    
    # Follow-up
    follow_up_date = Column(Date, nullable=True)
    follow_up_notes = Column(Text, nullable=True)
    
    # Rescheduling
    rescheduled_from = Column(UUID(as_uuid=True), ForeignKey("client_meetings.id"), nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    client = relationship("Client", back_populates="meetings")
    
    # Indexes
    __table_args__ = (
        Index('ix_client_meetings_client_id', 'client_id'),
        Index('ix_client_meetings_scheduled_at', 'scheduled_at'),
        Index('ix_client_meetings_status', 'status'),
        Index('ix_client_meetings_meeting_type', 'meeting_type'),
    )
    
    def __repr__(self):
        return f"<ClientMeeting(id={self.id}, client_id={self.client_id}, scheduled_at={self.scheduled_at})>"


class HiringRequirementCandidate(Base):
    """
    Junction table for candidates associated with hiring requirements
    """
    __tablename__ = "hiring_requirement_candidates"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hiring_requirement_id = Column(UUID(as_uuid=True), ForeignKey("hiring_requirements.id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    
    # Status
    status = Column(String(50), default="submitted", nullable=False)  # submitted, shortlisted, interviewed, rejected, hired
    status_changed_at = Column(DateTime(timezone=True), nullable=True)
    status_notes = Column(Text, nullable=True)
    
    # Match scoring
    match_score = Column(Integer, nullable=True)  # 0-100
    match_reasons = Column(ARRAY(String), default=[], nullable=False)
    
    # Interview tracking
    interview_count = Column(Integer, default=0, nullable=False)
    last_interview_date = Column(DateTime(timezone=True), nullable=True)
    
    # Feedback
    client_feedback = Column(Text, nullable=True)
    candidate_feedback = Column(Text, nullable=True)
    
    # Offer details
    offered_salary = Column(Numeric(12, 2), nullable=True)  # 12 digits with 2 decimal places
    offer_date = Column(Date, nullable=True)
    joining_date = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    hiring_requirement = relationship("HiringRequirement", back_populates="candidates")
    candidate = relationship("Candidate")
    
    # Indexes
    __table_args__ = (
        Index('ix_hiring_requirement_candidates_hiring_requirement_id', 'hiring_requirement_id'),
        Index('ix_hiring_requirement_candidates_candidate_id', 'candidate_id'),
        Index('ix_hiring_requirement_candidates_status', 'status'),
        Index('ix_hiring_requirement_candidates_match_score', 'match_score'),
        UniqueConstraint('hiring_requirement_id', 'candidate_id', name='uq_hiring_requirement_candidate'),
    )
    
    def __repr__(self):
        return f"<HiringRequirementCandidate(id={self.id}, hiring_requirement_id={self.hiring_requirement_id}, candidate_id={self.candidate_id})>"