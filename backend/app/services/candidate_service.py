"""
Candidate service for Thathvamasi HR Consultancy
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func, text

from app.models.candidate_model import (
    Candidate, CandidatePersonalDetails, CandidateProfessionalDetails,
    CandidateWorkExperience, CandidateEducation, CandidateMetadata,
    CandidateResume, CandidateNote, CandidateInterview
)
from app.schemas.candidate import (
    CandidateCreate, CandidateUpdate, CandidatePersonalDetailsUpdate,
    CandidateProfessionalDetailsUpdate, CandidateWorkExperienceBase,
    CandidateEducationBase, CandidateMetadataBase, CandidateFilterParams,
    PaginationParams
)
import logging

from app.core.database import get_db_session
from app.core.exceptions import NotFoundError, ValidationError
from app.core.validation import business_rules_validator, validation_utils
from app.core.logging_config import request_logger, database_logger
from app.services.db_file_service import DBFileService


logger = logging.getLogger(__name__)


class CandidateService:
    """Service for candidate operations"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def create_candidate(self, candidate_data: CandidateCreate, metadata: Optional[Dict[str, Any]] = None) -> Candidate:
        """
        Create a new candidate with all related data
        """
        import time
        start_time = time.time()
        
        try:
            logger.info(f"Creating new candidate: {candidate_data.personal_details.email}")
            
            # Validate business rules
            candidate_dict = candidate_data.dict()
            business_error = business_rules_validator.validate_candidate_registration(candidate_dict)
            if business_error:
                logger.warning(f"Business rule validation failed for {candidate_data.personal_details.email}: {business_error.message}")
                raise business_error
            
            # Validate email
            if not validation_utils.validate_email(candidate_data.personal_details.email):
                logger.warning(f"Invalid email address: {candidate_data.personal_details.email}")
                raise ValidationError("Invalid email address")
            
            # Validate phone number
            if not validation_utils.validate_phone_number(candidate_data.personal_details.mobile):
                logger.warning(f"Invalid phone number: {candidate_data.personal_details.mobile}")
                raise ValidationError("Invalid phone number. Indian mobile numbers should be 10 digits starting with 6-9")
            
            # Validate pincode if provided
            if candidate_data.personal_details.pincode:
                if not validation_utils.validate_pincode(candidate_data.personal_details.pincode):
                    logger.warning(f"Invalid pincode: {candidate_data.personal_details.pincode}")
                    raise ValidationError("Invalid pincode. Indian pincodes are 6 digits")
            
            # Validate date of birth for age
            if candidate_data.personal_details.date_of_birth:
                if not validation_utils.validate_age(candidate_data.personal_details.date_of_birth):
                    logger.warning(f"Invalid age for date of birth: {candidate_data.personal_details.date_of_birth}")
                    raise ValidationError("Age must be between 18 and 65 years")
            
            # Validate salary ranges
            if candidate_data.professional_details.current_salary:
                if not validation_utils.validate_salary(candidate_data.professional_details.current_salary):
                    logger.warning(f"Invalid current salary: {candidate_data.professional_details.current_salary}")
                    raise ValidationError("Current salary must be between 0 and 100,000,000")
            
            if candidate_data.professional_details.expected_salary:
                if not validation_utils.validate_salary(candidate_data.professional_details.expected_salary):
                    logger.warning(f"Invalid expected salary: {candidate_data.professional_details.expected_salary}")
                    raise ValidationError("Expected salary must be between 0 and 100,000,000")
            
            # Validate experience
            if candidate_data.professional_details.years_of_experience:
                if not validation_utils.validate_experience(candidate_data.professional_details.years_of_experience):
                    logger.warning(f"Invalid years of experience: {candidate_data.professional_details.years_of_experience}")
                    raise ValidationError("Years of experience must be between 0 and 50")
            
            # Validate skills
            if not validation_utils.validate_skills(candidate_data.professional_details.skills):
                logger.warning(f"Invalid skills list: {candidate_data.professional_details.skills}")
                raise ValidationError("Skills list is invalid. Maximum 20 skills allowed, each skill max 100 characters")
            
            # Validate tags
            if not validation_utils.validate_tags(candidate_data.tags):
                logger.warning(f"Invalid tags list: {candidate_data.tags}")
                raise ValidationError("Tags list is invalid. Maximum 10 tags allowed, each tag max 50 characters")
            
            # Start transaction
            async with self.db.begin():
                # Create main candidate record
                candidate = Candidate(
                    status=candidate_data.status,
                    priority=candidate_data.priority,
                    tags=candidate_data.tags,
                    source=candidate_data.source,
                    referrer=candidate_data.referrer,
                    consent_accepted=candidate_data.consent_accepted,
                    consent_accepted_at=datetime.utcnow() if candidate_data.consent_accepted else None
                )
                self.db.add(candidate)
                await self.db.flush()  # Get the candidate ID
                
                # Create personal details
                personal_details = CandidatePersonalDetails(
                    candidate_id=candidate.id,
                    full_name=candidate_data.personal_details.full_name,
                    email=candidate_data.personal_details.email,
                    mobile=candidate_data.personal_details.mobile,
                    whatsapp=candidate_data.personal_details.whatsapp,
                    current_location=candidate_data.personal_details.current_location,
                    preferred_location=candidate_data.personal_details.preferred_location,
                    date_of_birth=candidate_data.personal_details.date_of_birth,
                    gender=candidate_data.personal_details.gender,
                    marital_status=candidate_data.personal_details.marital_status,
                    address=candidate_data.personal_details.address,
                    city=candidate_data.personal_details.city,
                    state=candidate_data.personal_details.state,
                    country=candidate_data.personal_details.country,
                    pincode=candidate_data.personal_details.pincode,
                    emergency_contact_name=candidate_data.personal_details.emergency_contact_name,
                    emergency_contact_phone=candidate_data.personal_details.emergency_contact_phone,
                    emergency_contact_relation=candidate_data.personal_details.emergency_contact_relation
                )
                self.db.add(personal_details)
                
                # Create professional details
                professional_details = CandidateProfessionalDetails(
                    candidate_id=candidate.id,
                    highest_qualification=candidate_data.professional_details.highest_qualification,
                    specialization=candidate_data.professional_details.specialization,
                    university=candidate_data.professional_details.university,
                    graduation_year=candidate_data.professional_details.graduation_year,
                    total_experience=candidate_data.professional_details.total_experience,
                    years_of_experience=candidate_data.professional_details.years_of_experience,
                    current_company=candidate_data.professional_details.current_company,
                    current_designation=candidate_data.professional_details.current_designation,
                    current_salary=candidate_data.professional_details.current_salary,
                    current_salary_currency=candidate_data.professional_details.current_salary_currency,
                    expected_salary=candidate_data.professional_details.expected_salary,
                    expected_salary_currency=candidate_data.professional_details.expected_salary_currency,
                    notice_period=candidate_data.professional_details.notice_period,
                    notice_period_days=candidate_data.professional_details.notice_period_days,
                    skills=candidate_data.professional_details.skills,
                    preferred_job_role=candidate_data.professional_details.preferred_job_role,
                    preferred_industry=candidate_data.professional_details.preferred_industry,
                    job_type_preference=candidate_data.professional_details.job_type_preference,
                    work_preference=candidate_data.professional_details.work_preference,
                    languages_known=candidate_data.professional_details.languages_known,
                    certifications=candidate_data.professional_details.certifications,
                    achievements=candidate_data.professional_details.achievements
                )
                self.db.add(professional_details)
                await self.db.flush()  # Get the professional details ID
                
                # Create work experiences
                for work_exp in candidate_data.work_experiences:
                    work_experience = CandidateWorkExperience(
                        professional_details_id=professional_details.id,
                        company_name=work_exp.company_name,
                        company_industry=work_exp.company_industry,
                        company_size=work_exp.company_size,
                        designation=work_exp.designation,
                        department=work_exp.department,
                        employment_type=work_exp.employment_type,
                        start_date=work_exp.start_date,
                        end_date=work_exp.end_date,
                        is_current=work_exp.is_current,
                        location=work_exp.location,
                        work_mode=work_exp.work_mode,
                        responsibilities=work_exp.responsibilities,
                        achievements=work_exp.achievements,
                        salary=work_exp.salary,
                        salary_currency=work_exp.salary_currency,
                        reason_for_leaving=work_exp.reason_for_leaving,
                        references=work_exp.references
                    )
                    self.db.add(work_experience)
                
                # Create educations
                for edu in candidate_data.educations:
                    education = CandidateEducation(
                        professional_details_id=professional_details.id,
                        institution_name=edu.institution_name,
                        institution_type=edu.institution_type,
                        institution_location=edu.institution_location,
                        qualification=edu.qualification,
                        specialization=edu.specialization,
                        degree_type=edu.degree_type,
                        start_date=edu.start_date,
                        end_date=edu.end_date,
                        is_completed=edu.is_completed,
                        grade=edu.grade,
                        score=edu.score,
                        max_score=edu.max_score,
                        description=edu.description,
                        achievements=edu.achievements
                    )
                    self.db.add(education)
                
                # Create metadata
                if metadata or candidate_data.metadata:
                    meta_data = metadata or {}
                    if candidate_data.metadata:
                        meta_data.update(candidate_data.metadata.dict(exclude_none=True))
                    
                    candidate_metadata = CandidateMetadata(
                        candidate_id=candidate.id,
                        ip_address=meta_data.get('ip_address'),
                        user_agent=meta_data.get('user_agent'),
                        device_type=meta_data.get('device_type'),
                        browser=meta_data.get('browser'),
                        operating_system=meta_data.get('operating_system'),
                        referrer_url=meta_data.get('referrer_url'),
                        landing_page=meta_data.get('landing_page'),
                        utm_source=meta_data.get('utm_source'),
                        utm_medium=meta_data.get('utm_medium'),
                        utm_campaign=meta_data.get('utm_campaign'),
                        utm_term=meta_data.get('utm_term'),
                        utm_content=meta_data.get('utm_content'),
                        form_version=meta_data.get('form_version'),
                        form_fields=meta_data.get('form_fields')
                    )
                    self.db.add(candidate_metadata)
                
                # Commit transaction
                await self.db.commit()
                
                # Refresh and return candidate
                await self.db.refresh(candidate)
                
                duration_ms = (time.time() - start_time) * 1000
                logger.info(f"Successfully created candidate {candidate.id} in {duration_ms:.2f}ms")
                database_logger.log_connection("candidate_created", f"Candidate ID: {candidate.id}")
                
                return candidate
                
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create candidate {candidate_data.personal_details.email}: {str(e)}", exc_info=True)
            raise ValidationError(f"Failed to create candidate: {str(e)}")
    
    async def get_candidate(self, candidate_id: UUID) -> Optional[Candidate]:
        """
        Get candidate by ID with all relationships
        """
        stmt = (
            select(Candidate)
            .where(Candidate.id == candidate_id)
            .options(
                selectinload(Candidate.personal_details),
                selectinload(Candidate.professional_details),
                selectinload(Candidate.resumes),
                selectinload(Candidate.metadata),
                selectinload(Candidate.notes),
                selectinload(Candidate.interviews)
            )
        )
        result = await self.db.execute(stmt)
        candidate = result.scalar_one_or_none()
        
        if not candidate:
            raise NotFoundError(f"Candidate with ID {candidate_id} not found")
        
        return candidate
    
    async def get_candidate_detail(self, candidate_id: UUID) -> Dict[str, Any]:
        """
        Get candidate with all nested data (work experiences, educations)
        """
        # Get main candidate
        candidate = await self.get_candidate(candidate_id)
        
        # Get work experiences and educations if professional details exist
        result_data = {"candidate": candidate}
        
        if candidate.professional_details:
            # Get work experiences
            stmt_work = (
                select(CandidateWorkExperience)
                .where(CandidateWorkExperience.professional_details_id == candidate.professional_details.id)
                .order_by(CandidateWorkExperience.start_date.desc())
            )
            result_work = await self.db.execute(stmt_work)
            work_experiences = result_work.scalars().all()
            
            # Get educations
            stmt_edu = (
                select(CandidateEducation)
                .where(CandidateEducation.professional_details_id == candidate.professional_details.id)
                .order_by(CandidateEducation.end_date.desc())
            )
            result_edu = await self.db.execute(stmt_edu)
            educations = result_edu.scalars().all()
            
            result_data.update({
                "work_experiences": work_experiences,
                "educations": educations
            })
        
        return result_data
    
    async def list_candidates(
        self, 
        filters: CandidateFilterParams,
        pagination: PaginationParams
    ) -> Dict[str, Any]:
        """
        List candidates with filtering and pagination
        """
        # Build base query
        stmt = (
            select(Candidate)
            .join(CandidatePersonalDetails)
            .options(
                selectinload(Candidate.personal_details),
                selectinload(Candidate.professional_details),
                selectinload(Candidate.resumes),
                selectinload(Candidate.metadata)
            )
        )
        
        # Apply filters
        conditions = []
        
        if filters.status:
            conditions.append(Candidate.status == filters.status)
        
        if filters.priority:
            conditions.append(Candidate.priority == filters.priority)
        
        if filters.source:
            conditions.append(Candidate.source == filters.source)
        
        if filters.location:
            conditions.append(CandidatePersonalDetails.current_location.ilike(f"%{filters.location}%"))
        
        if filters.assigned_to:
            conditions.append(Candidate.assigned_to == filters.assigned_to)
        
        if filters.date_from:
            conditions.append(Candidate.created_at >= filters.date_from)
        
        if filters.date_to:
            conditions.append(Candidate.created_at <= filters.date_to)
        
        if filters.search:
            search_conditions = [
                CandidatePersonalDetails.full_name.ilike(f"%{filters.search}%"),
                CandidatePersonalDetails.email.ilike(f"%{filters.search}%"),
                CandidatePersonalDetails.mobile.ilike(f"%{filters.search}%")
            ]
            conditions.append(or_(*search_conditions))
        
        # Apply conditions
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        # Count total records
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (pagination.page - 1) * pagination.size
        stmt = stmt.offset(offset).limit(pagination.size)
        
        # Order by created date (newest first)
        stmt = stmt.order_by(Candidate.created_at.desc())
        
        # Execute query
        result = await self.db.execute(stmt)
        candidates = result.scalars().all()
        
        return {
            "items": candidates,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "total_pages": (total + pagination.size - 1) // pagination.size
        }
    
    async def update_candidate(self, candidate_id: UUID, update_data: CandidateUpdate) -> Candidate:
        """
        Update candidate information
        """
        candidate = await self.get_candidate(candidate_id)
        
        # Update fields if provided
        update_dict = update_data.dict(exclude_unset=True)
        
        # Validate status transition if status is being updated
        if 'status' in update_dict and update_dict['status'] != candidate.status:
            business_error = business_rules_validator.validate_status_transition(
                candidate.status, update_dict['status']
            )
            if business_error:
                raise business_error
            update_dict['status_changed_at'] = datetime.utcnow()
        
        # Validate tags if being updated
        if 'tags' in update_dict:
            if not validation_utils.validate_tags(update_dict['tags']):
                raise ValidationError("Tags list is invalid. Maximum 10 tags allowed, each tag max 50 characters")
        
        # Validate assignment if being updated
        if 'assigned_to' in update_dict:
            business_error = business_rules_validator.validate_assignment(
                candidate_id, update_dict['assigned_to']
            )
            if business_error:
                raise business_error
        
        for field, value in update_dict.items():
            setattr(candidate, field, value)
        
        self.db.add(candidate)
        await self.db.commit()
        await self.db.refresh(candidate)
        
        return candidate
    
    async def update_personal_details(self, candidate_id: UUID, update_data: CandidatePersonalDetailsUpdate) -> CandidatePersonalDetails:
        """
        Update candidate personal details
        """
        candidate = await self.get_candidate(candidate_id)
        
        if not candidate.personal_details:
            # Create personal details if they don't exist
            personal_details = CandidatePersonalDetails(
                candidate_id=candidate.id,
                **update_data.dict(exclude_unset=True)
            )
            self.db.add(personal_details)
        else:
            # Update existing personal details
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(candidate.personal_details, field, value)
            self.db.add(candidate.personal_details)
        
        await self.db.commit()
        await self.db.refresh(candidate.personal_details)
        
        return candidate.personal_details
    
    async def update_professional_details(self, candidate_id: UUID, update_data: CandidateProfessionalDetailsUpdate) -> CandidateProfessionalDetails:
        """
        Update candidate professional details
        """
        candidate = await self.get_candidate(candidate_id)
        
        if not candidate.professional_details:
            # Create professional details if they don't exist
            professional_details = CandidateProfessionalDetails(
                candidate_id=candidate.id,
                **update_data.dict(exclude_unset=True)
            )
            self.db.add(professional_details)
        else:
            # Update existing professional details
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(candidate.professional_details, field, value)
            self.db.add(candidate.professional_details)
        
        await self.db.commit()
        await self.db.refresh(candidate.professional_details)
        
        return candidate.professional_details
    
    async def add_work_experience(self, candidate_id: UUID, work_exp_data: CandidateWorkExperienceBase) -> CandidateWorkExperience:
        """
        Add work experience to candidate
        """
        candidate = await self.get_candidate(candidate_id)
        
        if not candidate.professional_details:
            raise ValidationError("Candidate must have professional details to add work experience")
        
        work_experience = CandidateWorkExperience(
            professional_details_id=candidate.professional_details.id,
            **work_exp_data.dict()
        )
        self.db.add(work_experience)
        
        await self.db.commit()
        await self.db.refresh(work_experience)
        
        return work_experience
    
    async def add_education(self, candidate_id: UUID, education_data: CandidateEducationBase) -> CandidateEducation:
        """
        Add education to candidate
        """
        candidate = await self.get_candidate(candidate_id)
        
        if not candidate.professional_details:
            raise ValidationError("Candidate must have professional details to add education")
        
        education = CandidateEducation(
            professional_details_id=candidate.professional_details.id,
            **education_data.dict()
        )
        self.db.add(education)
        
        await self.db.commit()
        await self.db.refresh(education)
        
        return education
    
    async def add_resume(self, candidate_id: UUID, file_data: Dict[str, Any]) -> CandidateResume:
        """
        Add resume to candidate
        """
        candidate = await self.get_candidate(candidate_id)
        
        # Mark all existing resumes as not primary
        if candidate.resumes:
            for resume in candidate.resumes:
                resume.is_primary = False
            self.db.add_all(candidate.resumes)
        
        # Create new resume
        resume = CandidateResume(
            candidate_id=candidate.id,
            file_url=file_data['file_url'],
            file_name=file_data['file_name'],
            file_size=file_data['file_size'],
            file_type=file_data['file_type'],
            cloudinary_id=file_data.get('cloudinary_id'),
            is_primary=True,
            uploaded_by=file_data.get('uploaded_by', 'candidate')
        )
        self.db.add(resume)
        
        await self.db.commit()
        await self.db.refresh(resume)
        
        return resume
    
    async def add_note(self, candidate_id: UUID, note_data: Dict[str, Any]) -> CandidateNote:
        """
        Add note to candidate
        """
        candidate = await self.get_candidate(candidate_id)
        
        note = CandidateNote(
            candidate_id=candidate.id,
            title=note_data.get('title'),
            content=note_data['content'],
            note_type=note_data.get('note_type', 'general'),
            created_by=note_data.get('created_by'),
            created_by_name=note_data.get('created_by_name'),
            is_private=note_data.get('is_private', False)
        )
        self.db.add(note)
        
        await self.db.commit()
        await self.db.refresh(note)
        
        return note
    
    async def delete_candidate(self, candidate_id: UUID) -> bool:
        """
        Delete candidate (soft delete if implemented)
        """
        candidate = await self.get_candidate(candidate_id)
        
        # For now, hard delete. In production, implement soft delete
        await self.db.delete(candidate)
        await self.db.commit()
        
        return True
    
    async def get_candidate_stats(self) -> Dict[str, Any]:
        """
        Get candidate statistics
        """
        # Status counts
        status_stmt = select(
            Candidate.status,
            func.count(Candidate.id).label('count')
        ).group_by(Candidate.status)
        
        status_result = await self.db.execute(status_stmt)
        status_counts = dict(status_result.all())
        
        # Total count
        total_stmt = select(func.count(Candidate.id))
        total_result = await self.db.execute(total_stmt)
        total = total_result.scalar()
        
        # New candidates today
        today_stmt = select(func.count(Candidate.id)).where(
            func.date(Candidate.created_at) == func.current_date()
        )
        today_result = await self.db.execute(today_stmt)
        today_count = today_result.scalar()
        
        # Monthly trend (last 6 months)
        monthly_trend = await self._get_monthly_trend()
        
        return {
            "total": total,
            "status_counts": status_counts,
            "today_count": today_count,
            "monthly_trend": monthly_trend
        }
    
    async def _get_monthly_trend(self) -> List[Dict[str, Any]]:
        """
        Get monthly registration trend
        """
        # SQL for monthly trend (PostgreSQL specific)
        trend_sql = text("""
            SELECT 
                TO_CHAR(DATE_TRUNC('month', created_at), 'YYYY-MM') as month,
                COUNT(*) as count
            FROM candidates
            WHERE created_at >= NOW() - INTERVAL '6 months'
            GROUP BY DATE_TRUNC('month', created_at)
            ORDER BY month DESC
        """)
        
        result = await self.db.execute(trend_sql)
        rows = result.fetchall()
        
        return [{"month": row[0], "count": row[1]} for row in rows]


# Utility functions to get service instances
async def get_candidate_service():
    """
    Dependency to get candidate service instance
    """
    async for session in get_db_session():
        yield CandidateService(session)


async def get_db_file_service():
    """
    Dependency to get DB file service instance
    """
    async for session in get_db_session():
        yield DBFileService(session)


# Need to import selectinload for relationships
from sqlalchemy.orm import selectinload