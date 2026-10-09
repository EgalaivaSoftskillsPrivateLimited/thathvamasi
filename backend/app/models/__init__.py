"""
Models package for Thathvamasi HR Consultancy (SQLAlchemy PostgreSQL models)
"""

from app.models.base import (
    BaseDBModel,
    BaseResponseModel,
    PaginatedResponse,
    ErrorResponse,
)
from app.models.user_model import (
    User,
    UserActivity,
)
from app.models.candidate_model import (
    Candidate,
    CandidatePersonalDetails,
    CandidateProfessionalDetails,
    CandidateResume,
    CandidateMetadata,
    CandidateWorkExperience,
    CandidateEducation,
    CandidateNote,
    CandidateInterview,
)
from app.models.client_model import (
    Client,
    HiringRequirement,
    JobDescriptionDocument,
    ClientContact,
    ClientDocument,
    ClientMetadata,
    ClientNote,
    ClientMeeting,
    HiringRequirementCandidate,
)
from app.models.blog_model import (
    Blog,
    BlogImage,
    BlogComment,
    BlogCategory,
    BlogTag,
)
from app.models.contact_model import ContactEnquiry
from app.models.db_mixins import (
    TimestampMixin,
    UUIDMixin,
    SoftDeleteMixin,
    AuditMixin,
)

__all__ = [
    # Base
    "BaseDBModel",
    "BaseResponseModel",
    "PaginatedResponse",
    "ErrorResponse",
    # User
    "User",
    "UserActivity",
    # Candidate
    "Candidate",
    "CandidatePersonalDetails",
    "CandidateProfessionalDetails",
    "CandidateResume",
    "CandidateMetadata",
    "CandidateWorkExperience",
    "CandidateEducation",
    "CandidateNote",
    "CandidateInterview",
    # Client
    "Client",
    "HiringRequirement",
    "JobDescriptionDocument",
    "ClientContact",
    "ClientDocument",
    "ClientMetadata",
    "ClientNote",
    "ClientMeeting",
    "HiringRequirementCandidate",
    # Blog
    "Blog",
    "BlogImage",
    "BlogComment",
    "BlogCategory",
    "BlogTag",
    # Mixins
    "TimestampMixin",
    "UUIDMixin",
    "SoftDeleteMixin",
    "AuditMixin",
]
