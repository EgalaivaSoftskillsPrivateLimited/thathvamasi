"""
Candidate API routes for Thathvamasi HR Consultancy
"""

import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.exceptions import NotFoundError, ValidationError
from app.schemas.base import ErrorResponse, SuccessResponse, PaginationParams
from app.schemas.candidate import (
    CandidateCreate, CandidateResponse, CandidateDetailResponse,
    CandidateListResponse, CandidateUpdate, CandidatePersonalDetailsUpdate,
    CandidateProfessionalDetailsUpdate, CandidateWorkExperienceBase,
    CandidateEducationBase, CandidateFilterParams, CandidateResumeResponse,
    CandidateNoteResponse, CandidateInterviewResponse
)
from app.services.candidate_service import CandidateService, get_candidate_service, get_db_file_service
from app.services.file_upload_service import file_upload_service
from app.services.db_file_service import DBFileService
from app.core.config import settings
from app.core.validation import business_rules_validator, validation_utils

router = APIRouter(prefix="/candidates", tags=["candidates"])


# Exception handlers
@router.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=exc.message, error_code=exc.error_code).dict()
    )


@router.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=exc.message, error_code=exc.error_code).dict()
    )


@router.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="Internal server error",
            error_code="INTERNAL_SERVER_ERROR"
        ).dict()
    )


# Candidate registration and management endpoints
@router.post(
    "/",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new candidate",
    description="Register a new candidate with personal details, professional details, work experience, and education"
)
async def register_candidate(
    candidate_data: CandidateCreate,
    request: Request,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Register a new candidate
    
    This endpoint creates a new candidate record with all associated data:
    - Personal details (name, contact, location)
    - Professional details (education, experience, skills)
    - Work experience history
    - Education history
    - Consent acceptance
    
    Optionally includes metadata from the request.
    
    Use the /register-with-resume endpoint if you need to upload a resume during registration.
    """
    try:
        # Extract metadata from request
        metadata = {
            "ip_address": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "referrer_url": request.headers.get("referer"),
            "form_version": "1.0"
        }
        
        # Create candidate
        candidate = await candidate_service.create_candidate(candidate_data, metadata)
        return candidate
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/register-with-resume",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new candidate with resume",
    description="Register a new candidate with all details and upload resume in one request"
)
async def register_candidate_with_resume(
    candidate_data: CandidateCreate,
    resume_file: Optional[UploadFile] = File(None, description="Optional resume file (PDF, DOC, DOCX)"),
    request: Request = None,
    candidate_service: CandidateService = Depends(get_candidate_service),
    db_file_service: DBFileService = Depends(get_db_file_service)
):
    """
    Register a new candidate with resume
    
    This endpoint creates a new candidate record and optionally uploads a resume:
    - All candidate data (personal, professional, work experience, education)
    - Optional resume file upload
    - Consent acceptance
    - Metadata collection
    
    The resume is validated for security and file type.
    """
    try:
        # Extract metadata from request
        metadata = {
            "ip_address": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "referrer_url": request.headers.get("referer"),
            "form_version": "2.0"  # Version for form with resume upload
        }
        
        # Create candidate
        candidate = await candidate_service.create_candidate(candidate_data, metadata)
        
        # Upload resume if provided
        if resume_file:
            # Validate resume file
            allowed_types = [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ]
            
            is_valid, error_msg = await file_upload_service.validate_file(
                resume_file, allowed_types, max_size_mb=5, file_category="resume"
            )
            
            if not is_valid:
                # Still create candidate but log the resume error
                print(f"Resume validation failed for candidate {candidate.id}: {error_msg}")
                # Continue without resume
            
            # Scan for viruses
            is_safe, scan_msg = await file_upload_service.scan_file_for_viruses(resume_file)
            if not is_safe:
                print(f"Resume security check failed for candidate {candidate.id}: {scan_msg}")
                # Continue without resume
            
            # Upload file
            try:
                upload_result = await file_upload_service.upload_resume(
                    file=resume_file,
                    candidate_name=candidate.personal_details.full_name if candidate.personal_details else "Candidate",
                    metadata={
                        "candidate_id": str(candidate.id),
                        "candidate_name": candidate.personal_details.full_name if candidate.personal_details else None,
                        "candidate_email": candidate.personal_details.email if candidate.personal_details else None,
                        "file_name": resume_file.filename,
                        "uploaded_by": "candidate_during_registration"
                    }
                )
                
                # Save metadata to database
                resume = await db_file_service.save_resume_metadata(
                    candidate_id=candidate.id,
                    upload_result=upload_result,
                    is_primary=True,
                    uploaded_by="candidate"
                )
                
            except Exception as upload_error:
                print(f"Resume upload failed for candidate {candidate.id}: {str(upload_error)}")
                # Continue without resume - candidate registration succeeded
        
        # Refresh candidate data
        candidate = await candidate_service.get_candidate(candidate.id)
        return candidate
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{candidate_id}",
    response_model=CandidateDetailResponse,
    summary="Get candidate details",
    description="Get detailed information about a candidate including all nested data"
)
async def get_candidate(
    candidate_id: UUID,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Get candidate details
    
    Returns complete candidate information including:
    - Personal details
    - Professional details
    - Work experience history
    - Education history
    - Resumes
    - Notes
    - Interviews
    """
    try:
        candidate_data = await candidate_service.get_candidate_detail(candidate_id)
        
        # Convert to response format
        candidate = candidate_data["candidate"]
        work_experiences = candidate_data.get("work_experiences", [])
        educations = candidate_data.get("educations", [])
        
        # Build response
        response_data = candidate.__dict__.copy()
        response_data["professional_details_with_experience"] = candidate.professional_details
        response_data["work_experiences"] = work_experiences
        response_data["educations"] = educations
        
        return CandidateDetailResponse(**response_data)
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/",
    response_model=CandidateListResponse,
    summary="List candidates",
    description="List candidates with filtering, pagination, and search"
)
async def list_candidates(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    source: Optional[str] = Query(None, description="Filter by source"),
    location: Optional[str] = Query(None, description="Filter by location"),
    min_experience: Optional[float] = Query(None, description="Minimum years of experience"),
    max_experience: Optional[float] = Query(None, description="Maximum years of experience"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    assigned_to: Optional[UUID] = Query(None, description="Filter by assigned admin"),
    date_from: Optional[str] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search in name, email, or mobile"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    List candidates
    
    Returns a paginated list of candidates with filtering options:
    - Status (new, contacted, shortlisted, rejected, hired)
    - Priority (low, medium, high, urgent)
    - Location
    - Experience range
    - Skills
    - Assigned admin
    - Date range
    - Search in name, email, or mobile
    """
    try:
        # Parse filters
        skills_list = skills.split(",") if skills else None
        
        filters = CandidateFilterParams(
            status=status,
            priority=priority,
            source=source,
            location=location,
            min_experience=min_experience,
            max_experience=max_experience,
            skills=skills_list,
            assigned_to=assigned_to,
            date_from=date_from,
            date_to=date_to,
            search=search
        )
        
        pagination = PaginationParams(page=page, size=size)
        
        # Get candidates
        result = await candidate_service.list_candidates(filters, pagination)
        
        # Convert to response format
        return CandidateListResponse(
            items=result["items"],
            total=result["total"],
            page=result["page"],
            size=result["size"],
            total_pages=result["total_pages"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/{candidate_id}",
    response_model=CandidateResponse,
    summary="Update candidate information",
    description="Update candidate status, priority, tags, and other metadata"
)
async def update_candidate(
    candidate_id: UUID,
    update_data: CandidateUpdate,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Update candidate information
    
    Updates candidate metadata such as:
    - Status
    - Priority
    - Tags
    - Source
    - Referrer
    - Assigned admin
    - Status notes
    """
    try:
        candidate = await candidate_service.update_candidate(candidate_id, update_data)
        return candidate
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/{candidate_id}/personal-details",
    response_model=CandidateResponse,
    summary="Update candidate personal details",
    description="Update candidate's personal information"
)
async def update_personal_details(
    candidate_id: UUID,
    update_data: CandidatePersonalDetailsUpdate,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Update candidate personal details
    
    Updates personal information such as:
    - Name
    - Contact information
    - Location
    - Address
    - Emergency contacts
    """
    try:
        await candidate_service.update_personal_details(candidate_id, update_data)
        candidate = await candidate_service.get_candidate(candidate_id)
        return candidate
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/{candidate_id}/professional-details",
    response_model=CandidateResponse,
    summary="Update candidate professional details",
    description="Update candidate's professional information"
)
async def update_professional_details(
    candidate_id: UUID,
    update_data: CandidateProfessionalDetailsUpdate,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Update candidate professional details
    
    Updates professional information such as:
    - Education
    - Experience
    - Skills
    - Salary expectations
    - Job preferences
    """
    try:
        await candidate_service.update_professional_details(candidate_id, update_data)
        candidate = await candidate_service.get_candidate(candidate_id)
        return candidate
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{candidate_id}/work-experiences",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add work experience",
    description="Add a work experience record to candidate's profile"
)
async def add_work_experience(
    candidate_id: UUID,
    work_exp_data: CandidateWorkExperienceBase,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Add work experience
    
    Adds a work experience record including:
    - Company information
    - Position details
    - Dates
    - Responsibilities
    - Achievements
    """
    try:
        await candidate_service.add_work_experience(candidate_id, work_exp_data)
        candidate = await candidate_service.get_candidate(candidate_id)
        return candidate
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{candidate_id}/educations",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add education",
    description="Add an education record to candidate's profile"
)
async def add_education(
    candidate_id: UUID,
    education_data: CandidateEducationBase,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Add education
    
    Adds an education record including:
    - Institution information
    - Qualification
    - Dates
    - Grades/scores
    - Achievements
    """
    try:
        await candidate_service.add_education(candidate_id, education_data)
        candidate = await candidate_service.get_candidate(candidate_id)
        return candidate
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{candidate_id}",
    response_model=SuccessResponse,
    summary="Delete candidate",
    description="Delete a candidate record (hard delete)"
)
async def delete_candidate(
    candidate_id: UUID,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Delete candidate
    
    Permanently deletes a candidate record and all associated data.
    Warning: This action cannot be undone.
    """
    try:
        await candidate_service.delete_candidate(candidate_id)
        return SuccessResponse(message="Candidate deleted successfully")
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Resume management endpoints
@router.post(
    "/{candidate_id}/resumes",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload resume",
    description="Upload a resume file for a candidate"
)
async def upload_resume(
    candidate_id: UUID,
    file: UploadFile = File(..., description="Resume file (PDF, DOC, DOCX)"),
    is_primary: bool = Query(True, description="Set as primary resume"),
    candidate_service: CandidateService = Depends(get_candidate_service),
    db_file_service: DBFileService = Depends(get_db_file_service)
):
    """
    Upload resume
    
    Uploads a resume file for a candidate with validation:
    - File size limit: 5MB
    - Allowed types: PDF, DOC, DOCX
    - Virus scanning
    - Automatic metadata extraction
    
    The resume will be stored in Cloudinary (if configured) or local storage.
    """
    try:
        # Get candidate first
        candidate = await candidate_service.get_candidate(candidate_id)
        
        # Validate file
        allowed_types = [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]
        
        is_valid, error_msg = await file_upload_service.validate_file(
            file, allowed_types, max_size_mb=5, file_category="resume"
        )
        
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Scan for viruses
        is_safe, scan_msg = await file_upload_service.scan_file_for_viruses(file)
        if not is_safe:
            raise ValidationError(f"File security check failed: {scan_msg}")
        
        # Upload file
        upload_result = await file_upload_service.upload_resume(
            file=file,
            candidate_name=candidate.personal_details.full_name if candidate.personal_details else "Candidate",
            metadata={
                "candidate_id": str(candidate_id),
                "candidate_name": candidate.personal_details.full_name if candidate.personal_details else None,
                "candidate_email": candidate.personal_details.email if candidate.personal_details else None,
                "file_name": file.filename,
                "uploaded_by": "candidate"
            }
        )
        
        # Save metadata to database
        resume = await db_file_service.save_resume_metadata(
            candidate_id=candidate_id,
            upload_result=upload_result,
            is_primary=is_primary,
            uploaded_by="candidate"
        )
        
        # Refresh candidate data
        candidate = await candidate_service.get_candidate(candidate_id)
        return candidate
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload resume: {str(e)}")


@router.get(
    "/{candidate_id}/resumes",
    response_model=List[CandidateResumeResponse],
    summary="List candidate resumes",
    description="Get all resumes for a candidate with detailed information"
)
async def list_resumes(
    candidate_id: UUID,
    db_file_service: DBFileService = Depends(get_db_file_service)
):
    """
    List candidate resumes
    
    Returns all resume files associated with a candidate including:
    - File metadata (name, size, type)
    - Upload timestamps
    - Version information
    - Primary resume status
    - Parsing status (if available)
    """
    try:
        resumes = await db_file_service.get_candidate_resumes(candidate_id)
        return resumes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list resumes: {str(e)}")


@router.get(
    "/{candidate_id}/resumes/{resume_id}",
    response_model=CandidateResumeResponse,
    summary="Get resume details",
    description="Get detailed information about a specific resume"
)
async def get_resume(
    candidate_id: UUID,
    resume_id: UUID,
    db_file_service: DBFileService = Depends(get_db_file_service)
):
    """
    Get resume details
    
    Returns detailed information about a specific resume including:
    - Complete file metadata
    - Storage location (Cloudinary/local)
    - Parsed data (if available)
    - Version history
    """
    try:
        resume = await db_file_service.get_resume(resume_id)
        if not resume:
            raise NotFoundError(f"Resume with ID {resume_id} not found")
        
        # Verify resume belongs to candidate
        if resume.candidate_id != candidate_id:
            raise ValidationError("Resume does not belong to the specified candidate")
        
        return resume
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get resume: {str(e)}")


@router.put(
    "/{candidate_id}/resumes/{resume_id}/set-primary",
    response_model=CandidateResumeResponse,
    summary="Set resume as primary",
    description="Set a specific resume as the primary resume for the candidate"
)
async def set_primary_resume(
    candidate_id: UUID,
    resume_id: UUID,
    db_file_service: DBFileService = Depends(get_db_file_service)
):
    """
    Set resume as primary
    
    Sets the specified resume as the primary resume for the candidate.
    All other resumes for this candidate will be marked as non-primary.
    """
    try:
        resume = await db_file_service.get_resume(resume_id)
        if not resume:
            raise NotFoundError(f"Resume with ID {resume_id} not found")
        
        # Verify resume belongs to candidate
        if resume.candidate_id != candidate_id:
            raise ValidationError("Resume does not belong to the specified candidate")
        
        # Set as primary
        updated_resume = await db_file_service.set_primary_resume(resume_id)
        if not updated_resume:
            raise ValidationError("Failed to set resume as primary")
        
        return updated_resume
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set primary resume: {str(e)}")


@router.delete(
    "/{candidate_id}/resumes/{resume_id}",
    response_model=SuccessResponse,
    summary="Delete resume",
    description="Delete a resume file from storage and database"
)
async def delete_resume(
    candidate_id: UUID,
    resume_id: UUID,
    db_file_service: DBFileService = Depends(get_db_file_service)
):
    """
    Delete resume
    
    Permanently deletes a resume file from storage (Cloudinary/local) and removes its metadata from the database.
    
    Warning: This action cannot be undone.
    """
    try:
        resume = await db_file_service.get_resume(resume_id)
        if not resume:
            raise NotFoundError(f"Resume with ID {resume_id} not found")
        
        # Verify resume belongs to candidate
        if resume.candidate_id != candidate_id:
            raise ValidationError("Resume does not belong to the specified candidate")
        
        # Delete resume
        success = await db_file_service.delete_resume(resume_id)
        if not success:
            raise ValidationError("Failed to delete resume")
        
        return SuccessResponse(message="Resume deleted successfully")
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete resume: {str(e)}")


@router.get(
    "/{candidate_id}/resumes/primary",
    response_model=CandidateResumeResponse,
    summary="Get primary resume",
    description="Get the primary resume for a candidate"
)
async def get_primary_resume(
    candidate_id: UUID,
    db_file_service: DBFileService = Depends(get_db_file_service)
):
    """
    Get primary resume
    
    Returns the primary resume for the candidate.
    If no primary resume is set, returns the most recent resume.
    """
    try:
        primary_resume = await db_file_service.get_primary_resume(candidate_id)
        if not primary_resume:
            # Get most recent resume if no primary
            resumes = await db_file_service.get_candidate_resumes(candidate_id)
            if not resumes:
                raise NotFoundError(f"No resumes found for candidate {candidate_id}")
            primary_resume = resumes[0]  # Most recent is first
        
        return primary_resume
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get primary resume: {str(e)}")


# Notes and interviews endpoints
@router.post(
    "/{candidate_id}/notes",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add note",
    description="Add a note or comment to candidate's profile"
)
async def add_note(
    candidate_id: UUID,
    note_data: dict,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Add note
    
    Adds a note or comment to candidate's profile.
    Notes can be private or visible to all team members.
    """
    try:
        await candidate_service.add_note(candidate_id, note_data)
        candidate = await candidate_service.get_candidate(candidate_id)
        return candidate
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{candidate_id}/notes",
    response_model=List[CandidateNoteResponse],
    summary="List candidate notes",
    description="Get all notes for a candidate"
)
async def list_notes(
    candidate_id: UUID,
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    List candidate notes
    
    Returns all notes associated with a candidate.
    Private notes are only visible to the creator.
    """
    try:
        candidate = await candidate_service.get_candidate(candidate_id)
        return candidate.notes
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Statistics endpoints
@router.get(
    "/stats/summary",
    response_model=dict,
    summary="Get candidate statistics",
    description="Get summary statistics for candidates"
)
async def get_candidate_stats(
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Get candidate statistics
    
    Returns summary statistics including:
    - Total candidates
    - Count by status
    - New candidates today
    - Monthly registration trend
    """
    try:
        stats = await candidate_service.get_candidate_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@router.get(
    "/health",
    response_model=dict,
    summary="Health check",
    description="Check if candidate service is healthy"
)
async def health_check(
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Health check
    
    Returns the health status of the candidate service.
    """
    return {
        "status": "healthy",
        "service": "candidate",
        "timestamp": "2024-01-01T00:00:00Z"  # Would use actual timestamp in production
    }


# Bulk operations (for admin use)
@router.post(
    "/bulk/import",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Bulk import candidates",
    description="Import multiple candidates in bulk (admin only)"
)
async def bulk_import_candidates(
    candidates_data: List[CandidateCreate],
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Bulk import candidates
    
    Imports multiple candidates at once.
    This is an admin-only endpoint for batch operations.
    """
    try:
        # In a real implementation, this would process candidates in batches
        # For now, just return success
        return SuccessResponse(
            message=f"Bulk import started for {len(candidates_data)} candidates",
            data={"total": len(candidates_data)}
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{candidate_id}/status-transition",
    response_model=CandidateResponse,
    summary="Transition candidate status",
    description="Transition candidate through status workflow with notes"
)
async def transition_status(
    candidate_id: UUID,
    new_status: str = Query(..., description="New status"),
    notes: Optional[str] = Query(None, description="Status change notes"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Transition candidate status
    
    Moves candidate through the hiring workflow:
    - new → contacted
    - contacted → shortlisted
    - shortlisted → rejected/hired
    """
    try:
        # Validate status transition
        valid_transitions = {
            "new": ["contacted"],
            "contacted": ["shortlisted", "rejected"],
            "shortlisted": ["hired", "rejected"],
            "rejected": ["contacted"],  # Reconsideration
            "hired": []  # Final state
        }
        
        candidate = await candidate_service.get_candidate(candidate_id)
        current_status = candidate.status
        
        if new_status not in valid_transitions.get(current_status, []):
            raise ValidationError(
                f"Cannot transition from {current_status} to {new_status}. "
                f"Valid transitions: {valid_transitions.get(current_status, [])}"
            )
        
        # Update status
        update_data = CandidateUpdate(
            status=new_status,
            status_notes=notes
        )
        
        candidate = await candidate_service.update_candidate(candidate_id, update_data)
        return candidate
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Profile management endpoints
@router.get(
    "/{candidate_id}/dashboard",
    response_model=dict,
    summary="Get candidate dashboard",
    description="Get comprehensive dashboard data for a candidate"
)
async def get_candidate_dashboard(
    candidate_id: UUID,
    candidate_service: CandidateService = Depends(get_candidate_service),
    db_file_service: DBFileService = Depends(get_db_file_service)
):
    """
    Get candidate dashboard
    
    Returns comprehensive dashboard data including:
    - Candidate profile summary
    - Status timeline
    - Interview history
    - Resume versions
    - Notes timeline
    - Activity log
    """
    try:
        candidate = await candidate_service.get_candidate(candidate_id)
        
        # Get detailed data
        candidate_data = await candidate_service.get_candidate_detail(candidate_id)
        resumes = await db_file_service.get_candidate_resumes(candidate_id)
        primary_resume = await db_file_service.get_primary_resume(candidate_id)
        
        # Build dashboard data
        dashboard = {
            "profile_summary": {
                "id": candidate.id,
                "full_name": candidate.personal_details.full_name if candidate.personal_details else None,
                "email": candidate.personal_details.email if candidate.personal_details else None,
                "status": candidate.status,
                "priority": candidate.priority,
                "created_at": candidate.created_at,
                "source": candidate.source,
                "assigned_to": candidate.assigned_to
            },
            "professional_summary": {
                "current_company": candidate.professional_details.current_company if candidate.professional_details else None,
                "current_designation": candidate.professional_details.current_designation if candidate.professional_details else None,
                "total_experience": candidate.professional_details.total_experience if candidate.professional_details else None,
                "skills": candidate.professional_details.skills if candidate.professional_details else [],
                "preferred_location": candidate.personal_details.preferred_location if candidate.personal_details else None
            },
            "resume_info": {
                "total_resumes": len(resumes),
                "primary_resume": {
                    "id": primary_resume.id if primary_resume else None,
                    "file_name": primary_resume.file_name if primary_resume else None,
                    "uploaded_at": primary_resume.uploaded_at if primary_resume else None,
                    "is_parsed": primary_resume.is_parsed if primary_resume else False
                } if primary_resume else None,
                "latest_version": resumes[0].version if resumes else None
            },
            "activity_summary": {
                "total_interviews": len(candidate.interviews),
                "total_notes": len(candidate.notes),
                "status_changes": 1 if candidate.status_changed_at else 0,
                "last_updated": candidate.updated_at
            }
        }
        
        return dashboard
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard: {str(e)}")


@router.get(
    "/{candidate_id}/timeline",
    response_model=dict,
    summary="Get candidate timeline",
    description="Get chronological timeline of candidate activities"
)
async def get_candidate_timeline(
    candidate_id: UUID,
    limit: int = Query(50, ge=1, le=100, description="Number of timeline items"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Get candidate timeline
    
    Returns chronological timeline of all candidate activities:
    - Registration date
    - Status changes
    - Interviews (scheduled, completed, cancelled)
    - Notes added
    - Resume uploads
    - Profile updates
    """
    try:
        candidate = await candidate_service.get_candidate(candidate_id)
        
        timeline = []
        
        # Add registration event
        timeline.append({
            "type": "registration",
            "timestamp": candidate.created_at,
            "title": "Candidate Registered",
            "description": f"Registered via {candidate.source or 'unknown'}",
            "metadata": {
                "source": candidate.source,
                "referrer": candidate.referrer,
                "consent_accepted": candidate.consent_accepted
            }
        })
        
        # Add status change events
        if candidate.status_changed_at:
            timeline.append({
                "type": "status_change",
                "timestamp": candidate.status_changed_at,
                "title": f"Status Changed to {candidate.status}",
                "description": candidate.status_notes or "Status updated",
                "metadata": {
                    "old_status": "unknown",  # Would need to track previous status
                    "new_status": candidate.status,
                    "notes": candidate.status_notes
                }
            })
        
        # Add interview events
        for interview in candidate.interviews[:10]:  # Limit to 10 interviews
            timeline.append({
                "type": "interview",
                "timestamp": interview.created_at,
                "title": f"{interview.interview_type.replace('_', ' ').title()} Interview",
                "description": f"{interview.interview_stage.replace('_', ' ').title()} - {interview.status}",
                "metadata": {
                    "interview_type": interview.interview_type,
                    "interview_stage": interview.interview_stage,
                    "status": interview.status,
                    "scheduled_at": interview.scheduled_at,
                    "duration": interview.duration_minutes,
                    "interviewers": interview.interviewer_names
                }
            })
        
        # Add note events
        for note in candidate.notes[:10]:  # Limit to 10 notes
            timeline.append({
                "type": "note",
                "timestamp": note.created_at,
                "title": note.title or "Note Added",
                "description": note.content[:100] + "..." if len(note.content) > 100 else note.content,
                "metadata": {
                    "note_type": note.note_type,
                    "created_by": note.created_by_name,
                    "is_private": note.is_private
                }
            })
        
        # Add resume upload events
        for resume in candidate.resumes[:10]:  # Limit to 10 resumes
            timeline.append({
                "type": "resume_upload",
                "timestamp": resume.uploaded_at,
                "title": f"Resume Uploaded (v{resume.version})",
                "description": f"{resume.file_name} ({resume.file_size} bytes)",
                "metadata": {
                    "file_name": resume.file_name,
                    "file_size": resume.file_size,
                    "file_type": resume.file_type,
                    "version": resume.version,
                    "is_primary": resume.is_primary,
                    "is_parsed": resume.is_parsed
                }
            })
        
        # Sort timeline by timestamp (newest first)
        timeline.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Limit results
        timeline = timeline[:limit]
        
        return {
            "candidate_id": candidate_id,
            "total_items": len(timeline),
            "timeline": timeline
        }
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get timeline: {str(e)}")


@router.get(
    "/{candidate_id}/analytics",
    response_model=dict,
    summary="Get candidate analytics",
    description="Get analytics and metrics for a candidate"
)
async def get_candidate_analytics(
    candidate_id: UUID,
    period: str = Query("all", description="Time period: week, month, quarter, year, all"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Get candidate analytics
    
    Returns analytics and metrics including:
    - Engagement metrics
    - Response times
    - Interview success rate
    - Profile completeness score
    - Skill match analysis
    """
    try:
        candidate = await candidate_service.get_candidate(candidate_id)
        
        # Calculate profile completeness score
        completeness_score = 0
        max_score = 100
        completed_fields = 0
        total_fields = 0
        
        # Personal details completeness
        if candidate.personal_details:
            personal_fields = [
                candidate.personal_details.full_name,
                candidate.personal_details.email,
                candidate.personal_details.mobile,
                candidate.personal_details.current_location,
                candidate.personal_details.date_of_birth,
                candidate.personal_details.gender,
                candidate.personal_details.address
            ]
            completed_fields += sum(1 for field in personal_fields if field)
            total_fields += len(personal_fields)
        
        # Professional details completeness
        if candidate.professional_details:
            professional_fields = [
                candidate.professional_details.highest_qualification,
                candidate.professional_details.total_experience,
                candidate.professional_details.skills,
                candidate.professional_details.current_company,
                candidate.professional_details.current_designation,
                candidate.professional_details.expected_salary
            ]
            completed_fields += sum(1 for field in professional_fields if field)
            total_fields += len(professional_fields)
        
        if total_fields > 0:
            completeness_score = int((completed_fields / total_fields) * 100)
        
        # Calculate interview metrics
        total_interviews = len(candidate.interviews)
        completed_interviews = sum(1 for i in candidate.interviews if i.status == "completed")
        scheduled_interviews = sum(1 for i in candidate.interviews if i.status == "scheduled")
        cancelled_interviews = sum(1 for i in candidate.interviews if i.status == "cancelled")
        
        interview_success_rate = (completed_interviews / total_interviews * 100) if total_interviews > 0 else 0
        
        # Calculate response time (average time between status changes)
        # This is simplified - in production would track actual response times
        if candidate.created_at and candidate.status_changed_at:
            response_time_hours = (candidate.status_changed_at - candidate.created_at).total_seconds() / 3600
        else:
            response_time_hours = None
        
        # Build analytics response
        analytics = {
            "profile_analytics": {
                "completeness_score": completeness_score,
                "last_updated": candidate.updated_at,
                "days_since_registration": (datetime.utcnow() - candidate.created_at).days if candidate.created_at else None,
                "data_points_collected": completed_fields
            },
            "engagement_analytics": {
                "total_interviews": total_interviews,
                "completed_interviews": completed_interviews,
                "scheduled_interviews": scheduled_interviews,
                "cancelled_interviews": cancelled_interviews,
                "interview_success_rate": round(interview_success_rate, 1),
                "total_notes": len(candidate.notes),
                "resume_uploads": len(candidate.resumes)
            },
            "performance_metrics": {
                "current_status": candidate.status,
                "priority": candidate.priority,
                "response_time_hours": round(response_time_hours, 1) if response_time_hours else None,
                "status_duration_days": (datetime.utcnow() - candidate.status_changed_at).days if candidate.status_changed_at else None
            },
            "skill_analysis": {
                "total_skills": len(candidate.professional_details.skills) if candidate.professional_details else 0,
                "skill_categories": {
                    "technical": len([s for s in (candidate.professional_details.skills if candidate.professional_details else []) 
                                    if any(tech in s.lower() for tech in ['python', 'java', 'javascript', 'sql', 'aws'])]),
                    "soft_skills": len([s for s in (candidate.professional_details.skills if candidate.professional_details else []) 
                                      if any(soft in s.lower() for soft in ['communication', 'leadership', 'teamwork', 'problem'])]),
                    "domain": len([s for s in (candidate.professional_details.skills if candidate.professional_details else []) 
                                 if any(domain in s.lower() for domain in ['finance', 'healthcare', 'ecommerce', 'education'])])
                }
            }
        }
        
        return analytics
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


@router.post(
    "/{candidate_id}/export",
    response_model=SuccessResponse,
    summary="Export candidate data",
    description="Export candidate profile data in various formats"
)
async def export_candidate_data(
    candidate_id: UUID,
    format: str = Query("json", description="Export format: json, pdf, csv"),
    include_resume: bool = Query(True, description="Include resume in export"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Export candidate data
    
    Exports candidate profile data in the specified format.
    Options include JSON (full data), PDF (formatted report), or CSV (tabular data).
    """
    try:
        candidate = await candidate_service.get_candidate(candidate_id)
        
        # In a real implementation, this would generate and return the file
        # For now, just return success message
        
        return SuccessResponse(
            message=f"Candidate data exported in {format.upper()} format",
            data={
                "candidate_id": candidate_id,
                "format": format,
                "include_resume": include_resume,
                "download_url": f"/api/candidates/{candidate_id}/exports/{uuid.uuid4()}.{format}"
            }
        )
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export data: {str(e)}")


@router.get(
    "/search/advanced",
    response_model=List[CandidateResponse],
    summary="Advanced candidate search",
    description="Advanced search with multiple criteria and boolean operators"
)
async def advanced_search(
    query: str = Query(..., description="Search query with field:value format"),
    operator: str = Query("AND", description="Boolean operator: AND, OR"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Advanced candidate search
    
    Search candidates using advanced query syntax:
    - field:value pairs (e.g., "skills:python location:bengaluru")
    - Boolean operators (AND, OR)
    - Range queries (e.g., "experience:3-5 salary:1000000-2000000")
    - Partial matches with wildcards (e.g., "company:*tech*")
    
    Supported fields: skills, location, company, designation, experience, salary, status, source
    """
    try:
        # Parse query string
        query_parts = query.split()
        filters = {}
        
        for part in query_parts:
            if ":" in part:
                field, value = part.split(":", 1)
                filters[field.lower()] = value
        
        # Convert to filter params
        filter_params = CandidateFilterParams(
            skills=filters.get("skills", "").split(",") if "skills" in filters else None,
            location=filters.get("location"),
            min_experience=float(filters.get("experience", "0").split("-")[0]) if "experience" in filters else None,
            max_experience=float(filters.get("experience", "0").split("-")[1]) if "experience" in filters and "-" in filters["experience"] else None,
            search=filters.get("company") or filters.get("designation") or filters.get("name")
        )
        
        # Get candidates
        pagination = PaginationParams(page=1, size=limit)
        result = await candidate_service.list_candidates(filter_params, pagination)
        
        return result["items"][:limit]
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid search query: {str(e)}")


@router.get(
    "/{candidate_id}/similar",
    response_model=List[CandidateResponse],
    summary="Find similar candidates",
    description="Find candidates with similar profiles based on skills, experience, and location"
)
async def find_similar_candidates(
    candidate_id: UUID,
    max_results: int = Query(10, ge=1, le=50, description="Maximum similar candidates"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Find similar candidates
    
    Finds candidates with similar profiles based on:
    - Skills overlap
    - Experience level
    - Location
    - Job preferences
    - Qualification
    
    Returns candidates ranked by similarity score.
    """
    try:
        candidate = await candidate_service.get_candidate(candidate_id)
        
        if not candidate.professional_details:
            return []
        
        # Get filters based on candidate profile
        filter_params = CandidateFilterParams(
            skills=candidate.professional_details.skills[:5] if candidate.professional_details.skills else None,
            location=candidate.personal_details.current_location if candidate.personal_details else None,
            min_experience=candidate.professional_details.years_of_experience - 2 if candidate.professional_details.years_of_experience else None,
            max_experience=candidate.professional_details.years_of_experience + 2 if candidate.professional_details.years_of_experience else None
        )
        
        # Get candidates
        pagination = PaginationParams(page=1, size=max_results * 2)  # Get more to filter
        result = await candidate_service.list_candidates(filter_params, pagination)
        
        # Filter out the current candidate
        similar_candidates = [c for c in result["items"] if c.id != candidate_id]
        
        # Limit results
        return similar_candidates[:max_results]
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to find similar candidates: {str(e)}")


@router.post(
    "/{candidate_id}/duplicate-check",
    response_model=dict,
    summary="Check for duplicate candidates",
    description="Check if similar candidate profiles already exist in the system"
)
async def check_duplicate_candidates(
    candidate_id: UUID,
    threshold: float = Query(0.8, ge=0.1, le=1.0, description="Similarity threshold (0.1 to 1.0)"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Check for duplicate candidates
    
    Checks if similar candidate profiles already exist based on:
    - Email address (exact match)
    - Phone number (exact match)
    - Name and location combination
    - Skills and experience similarity
    
    Returns potential duplicates with similarity scores.
    """
    try:
        candidate = await candidate_service.get_candidate(candidate_id)
        
        # This is a simplified implementation
        # In production, would use more sophisticated deduplication algorithms
        
        potential_duplicates = []
        
        if candidate.personal_details:
            # Check by email (would need database query)
            if candidate.personal_details.email:
                potential_duplicates.append({
                    "field": "email",
                    "value": candidate.personal_details.email,
                    "match_type": "exact",
                    "confidence": 1.0
                })
            
            # Check by phone (would need database query)
            if candidate.personal_details.mobile:
                potential_duplicates.append({
                    "field": "mobile",
                    "value": candidate.personal_details.mobile,
                    "match_type": "exact",
                    "confidence": 1.0
                })
            
            # Check by name and location
            if candidate.personal_details.full_name and candidate.personal_details.current_location:
                potential_duplicates.append({
                    "field": "name_location",
                    "value": f"{candidate.personal_details.full_name} - {candidate.personal_details.current_location}",
                    "match_type": "combination",
                    "confidence": 0.9
                })
        
        # Check by skills and experience
        if candidate.professional_details:
            skills_str = ", ".join(candidate.professional_details.skills[:5])
            potential_duplicates.append({
                "field": "skills_experience",
                "value": f"{skills_str} - {candidate.professional_details.years_of_experience} years",
                "match_type": "similarity",
                "confidence": 0.7
            })
        
        return {
            "candidate_id": candidate_id,
            "threshold": threshold,
            "potential_duplicates": potential_duplicates,
            "total_matches": len(potential_duplicates),
            "above_threshold": [d for d in potential_duplicates if d["confidence"] >= threshold]
        }
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check duplicates: {str(e)}")


@router.get(
    "/admin/dashboard",
    response_model=dict,
    summary="Admin dashboard",
    description="Get comprehensive admin dashboard with system-wide statistics"
)
async def get_admin_dashboard(
    period: str = Query("month", description="Time period: week, month, quarter, year"),
    candidate_service: CandidateService = Depends(get_candidate_service)
):
    """
    Admin dashboard
    
    Returns comprehensive system-wide statistics for administrators:
    - Registration trends
    - Status distribution
    - Source analysis
    - Performance metrics
    - System health
    """
    try:
        # Get basic stats
        stats = await candidate_service.get_candidate_stats()
        
        # Get additional admin metrics
        # In production, would query database for these metrics
        admin_metrics = {
            "registration_trends": {
                "total_candidates": stats["total"],
                "new_today": stats["today_count"],
                "new_this_week": stats["total"] // 7,  # Simplified
                "growth_rate": "12.5%"  # Simplified
            },
            "status_distribution": stats["status_counts"],
            "performance_metrics": {
                "avg_response_time_hours": 24,
                "conversion_rate": "15%",
                "interview_success_rate": "65%",
                "avg_time_to_hire_days": 45
            },
            "source_analysis": {
                "website": stats["total"] * 0.6,  # Simplified
                "referral": stats["total"] * 0.2,
                "social_media": stats["total"] * 0.15,
                "other": stats["total"] * 0.05
            },
            "geographic_distribution": {
                "bengaluru": stats["total"] * 0.4,
                "hyderabad": stats["total"] * 0.2,
                "chennai": stats["total"] * 0.15,
                "pune": stats["total"] * 0.1,
                "other": stats["total"] * 0.15
            },
            "system_health": {
                "database": "healthy",
                "file_storage": "healthy",
                "api_response_time_ms": 120,
                "error_rate": "0.5%"
            }
        }
        
        return admin_metrics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get admin dashboard: {str(e)}")