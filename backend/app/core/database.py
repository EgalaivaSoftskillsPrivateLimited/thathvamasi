    """
PostgreSQL database configuration for Thathvamasi HR Consultancy
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declared_attr
from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Create metadata with naming convention
metadata = MetaData(naming_convention=convention)

# Create base class for models with the metadata
Base = declarative_base(metadata=metadata)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields db sessions
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Alias for backward compatibility
get_db_session = get_db


async def init_db():
    """
    Initialize database - create tables
    """
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    
    # Create database if it doesn't exist (synchronous)
    sync_engine = create_engine(settings.DATABASE_URL_SYNC)
    
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)
        print(f"✅ Created database: {settings.POSTGRES_DB}")
    
    sync_engine.dispose()
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print(f"✅ Database tables created successfully")


async def close_db():
    """
    Close database connections
    """
    await engine.dispose()
    print("✅ Database connections closed")


# For backward compatibility and easier imports
db = Base  # Alias for Base
session = AsyncSessionLocal  # Alias for session factory


# Import models here to ensure they're registered with Base
from app.models.user_model import User, UserActivity
from app.models.candidate_model import (
    Candidate, CandidatePersonalDetails, CandidateProfessionalDetails,
    CandidateResume, CandidateMetadata, CandidateWorkExperience,
    CandidateEducation, CandidateNote, CandidateInterview
)
from app.models.client_model import (
    Client, HiringRequirement, JobDescriptionDocument, ClientContact,
    ClientDocument, ClientMetadata, ClientNote, ClientMeeting,
    HiringRequirementCandidate
)
from app.models.blog_model import (
    Blog, BlogImage, BlogComment, BlogCategory, BlogTag
)

__all__ = [
    "Base", "engine", "AsyncSessionLocal", "get_db", "get_db_session", "init_db", "close_db", "metadata",
    "db", "session", "declared_attr"
]