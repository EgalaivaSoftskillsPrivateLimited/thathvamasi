"""
File upload API endpoints with PostgreSQL integration
"""

import uuid
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.file_upload_service import file_upload_service
from app.services.db_file_service import DBFileService
from app.core.security import rate_limit_public, check_admin_permissions
from app.core.database import get_db
from app.models.user_model import User
from app.models.base import BaseResponseModel
from app.utils.helpers import sanitize_filename

router = APIRouter()


@router.post("/resume", response_model=BaseResponseModel)
@rate_limit_public
async def upload_resume(
    file: UploadFile = File(..., description="Resume file (PDF, DOC, DOCX, max 5MB)"),
    candidate_id: str = Form(..., description="Candidate ID (UUID)"),
    is_primary: bool = Form(True, description="Whether this is the primary resume"),
    uploaded_by: Optional[str] = Form(None, description="Who uploaded the resume"),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload candidate resume and save metadata to PostgreSQL
    
    - **file**: Resume file (PDF, DOC, DOCX)
    - **candidate_id**: Candidate ID (UUID)
    - **is_primary**: Whether this is the primary resume
    - **uploaded_by**: Optional - who uploaded the resume
    """
    try:
        # Validate file is provided
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # Validate candidate_id is a valid UUID
        try:
            candidate_uuid = uuid.UUID(candidate_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid candidate ID format"
            )
        
        # Upload resume to Cloudinary/local storage
        upload_result = await file_upload_service.upload_resume(
            file, "Candidate", None  # We'll use candidate name from DB
        )
        
        # Save metadata to PostgreSQL
        db_file_service = DBFileService(db)
        resume = await db_file_service.save_resume_metadata(
            candidate_id=candidate_uuid,
            upload_result=upload_result,
            is_primary=is_primary,
            uploaded_by=uploaded_by
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Resume uploaded successfully",
                "data": {
                    "resume_id": str(resume.id),
                    "candidate_id": str(resume.candidate_id),
                    "file_url": resume.file_url,
                    "file_name": resume.file_name,
                    "file_size": resume.file_size,
                    "file_type": resume.file_type,
                    "version": resume.version,
                    "is_primary": resume.is_primary,
                    "uploaded_at": resume.uploaded_at.isoformat(),
                    "storage_info": upload_result
                }
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload resume: {str(e)}"
        )


@router.post("/job-description", response_model=BaseResponseModel)
@rate_limit_public
async def upload_job_description(
    file: UploadFile = File(..., description="Job description file (PDF, DOC, DOCX, max 10MB)"),
    hiring_requirement_id: str = Form(..., description="Hiring requirement ID (UUID)"),
    is_primary: bool = Form(True, description="Whether this is the primary JD"),
    uploaded_by: Optional[str] = Form(None, description="Who uploaded the JD"),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload job description file and save metadata to PostgreSQL
    
    - **file**: Job description file (PDF, DOC, DOCX)
    - **hiring_requirement_id**: Hiring requirement ID (UUID)
    - **is_primary**: Whether this is the primary JD
    - **uploaded_by**: Optional - who uploaded the JD
    """
    try:
        # Validate file is provided
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # Validate hiring_requirement_id is a valid UUID
        try:
            hr_uuid = uuid.UUID(hiring_requirement_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid hiring requirement ID format"
            )
        
        # Upload job description to Cloudinary/local storage
        upload_result = await file_upload_service.upload_job_description(
            file, "Company", "Position Title", None  # We'll get details from DB
        )
        
        # Save metadata to PostgreSQL
        db_file_service = DBFileService(db)
        jd = await db_file_service.save_jd_metadata(
            hiring_requirement_id=hr_uuid,
            upload_result=upload_result,
            is_primary=is_primary,
            uploaded_by=uploaded_by
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Job description uploaded successfully",
                "data": {
                    "jd_id": str(jd.id),
                    "hiring_requirement_id": str(jd.hiring_requirement_id),
                    "file_url": jd.file_url,
                    "file_name": jd.file_name,
                    "file_size": jd.file_size,
                    "file_type": jd.file_type,
                    "version": jd.version,
                    "is_primary": jd.is_primary,
                    "uploaded_at": jd.uploaded_at.isoformat(),
                    "storage_info": upload_result
                }
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload job description: {str(e)}"
        )


@router.post("/blog-image", response_model=BaseResponseModel)
@rate_limit_public
async def upload_blog_image(
    file: UploadFile = File(..., description="Blog image (JPEG, PNG, GIF, WebP, max 5MB)"),
    blog_id: str = Form(..., description="Blog ID (UUID)"),
    alt_text: Optional[str] = Form(None, description="Image alt text for accessibility"),
    caption: Optional[str] = Form(None, description="Image caption"),
    is_featured: bool = Form(False, description="Whether this is a featured image"),
    uploaded_by: Optional[str] = Form(None, description="Who uploaded the image"),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload blog image and save metadata to PostgreSQL
    
    - **file**: Image file (JPEG, PNG, GIF, WebP)
    - **blog_id**: Blog ID (UUID)
    - **alt_text**: Optional image alt text for accessibility
    - **caption**: Optional image caption
    - **is_featured**: Whether this is a featured image
    - **uploaded_by**: Optional - who uploaded the image
    """
    try:
        # Validate file is provided
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # Validate blog_id is a valid UUID
        try:
            blog_uuid = uuid.UUID(blog_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid blog ID format"
            )
        
        # Get blog title for context (optional - can fetch from DB)
        blog_title = "Blog Image"  # In production, fetch from DB
        
        # Upload blog image to Cloudinary/local storage
        upload_result = await file_upload_service.upload_blog_image(
            file, blog_title, is_featured, None
        )
        
        # Save metadata to PostgreSQL
        db_file_service = DBFileService(db)
        image = await db_file_service.save_blog_image_metadata(
            blog_id=blog_uuid,
            upload_result=upload_result,
            alt_text=alt_text,
            caption=caption,
            is_featured=is_featured,
            uploaded_by=uploaded_by
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Blog image uploaded successfully",
                "data": {
                    "image_id": str(image.id),
                    "blog_id": str(image.blog_id),
                    "image_url": image.image_url,
                    "thumbnail_url": image.thumbnail_url,
                    "original_filename": image.original_filename,
                    "file_size": image.file_size,
                    "file_type": image.file_type,
                    "width": image.width,
                    "height": image.height,
                    "alt_text": image.alt_text,
                    "caption": image.caption,
                    "is_featured": image.is_featured,
                    "uploaded_at": image.uploaded_at.isoformat(),
                    "storage_info": upload_result
                }
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload blog image: {str(e)}"
        )


@router.post("/general", response_model=BaseResponseModel)
@rate_limit_public
async def upload_general_file(
    file: UploadFile = File(..., description="General file (max 10MB)"),
    category: str = Form(..., description="File category"),
    description: str = Form(..., description="File description"),
    metadata: Optional[str] = Form(None, description="Additional metadata as JSON string")
):
    """
    Upload general file
    
    - **file**: Any file (max 10MB)
    - **category**: File category (e.g., 'document', 'image', 'other')
    - **description**: File description
    - **metadata**: Optional metadata in JSON format
    """
    try:
        # Validate file is provided
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        
        # Validate category
        if not category or len(category) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category must be between 1 and 50 characters"
            )
        
        # Upload general file
        upload_result = await file_upload_service.upload_general_file(
            file, category, description, metadata
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "File uploaded successfully",
                "data": upload_result
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.delete("/resume/{resume_id}")
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(check_admin_permissions),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete resume file (Admin only)
    
    - **resume_id**: Resume ID (UUID)
    """
    try:
        # Validate resume_id is a valid UUID
        try:
            resume_uuid = uuid.UUID(resume_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid resume ID format"
            )
        
        # Delete resume using database service
        db_file_service = DBFileService(db)
        success = await db_file_service.delete_resume(resume_uuid)
        
        if success:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "message": "Resume deleted successfully"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete resume: {str(e)}"
        )


@router.get("/info/{file_identifier}")
async def get_file_info(
    file_identifier: str,
    resource_type: str = "raw",
    current_user: User = Depends(check_admin_permissions)
):
    """
    Get file information (Admin only)
    
    - **file_identifier**: File identifier
    - **resource_type**: Resource type (Cloudinary only)
    """
    try:
        # Get file info
        file_info = await file_upload_service.get_file_info(file_identifier, resource_type)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": file_info
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get file info: {str(e)}"
        )


@router.get("/storage/usage")
async def get_storage_usage(
    current_user: User = Depends(check_admin_permissions),
    db: AsyncSession = Depends(get_db)
):
    """
    Get storage usage statistics (Admin only)
    """
    try:
        # Get storage usage from file service
        storage_usage = file_upload_service.get_storage_usage()
        
        # Get file statistics from database
        db_file_service = DBFileService(db)
        file_stats = await db_file_service.get_file_stats()
        
        # Combine both
        usage_info = {
            **storage_usage,
            "database_stats": file_stats
        }
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": usage_info
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get storage usage: {str(e)}"
        )


@router.get("/resume/{resume_id}")
async def get_resume_info(
    resume_id: str,
    current_user: User = Depends(check_admin_permissions),
    db: AsyncSession = Depends(get_db)
):
    """
    Get resume information (Admin only)
    
    - **resume_id**: Resume ID (UUID)
    """
    try:
        # Validate resume_id is a valid UUID
        try:
            resume_uuid = uuid.UUID(resume_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid resume ID format"
            )
        
        # Get resume from database
        db_file_service = DBFileService(db)
        resume = await db_file_service.get_resume(resume_uuid)
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": {
                    "id": str(resume.id),
                    "candidate_id": str(resume.candidate_id),
                    "file_url": resume.file_url,
                    "file_name": resume.file_name,
                    "file_size": resume.file_size,
                    "file_type": resume.file_type,
                    "cloudinary_id": resume.cloudinary_id,
                    "version": resume.version,
                    "is_primary": resume.is_primary,
                    "uploaded_by": resume.uploaded_by,
                    "uploaded_at": resume.uploaded_at.isoformat(),
                    "is_parsed": resume.is_parsed,
                    "parsed_data": resume.parsed_data
                }
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get resume info: {str(e)}"
        )


@router.get("/candidate/{candidate_id}/resumes")
async def get_candidate_resumes(
    candidate_id: str,
    current_user: User = Depends(check_admin_permissions),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all resumes for a candidate (Admin only)
    
    - **candidate_id**: Candidate ID (UUID)
    """
    try:
        # Validate candidate_id is a valid UUID
        try:
            candidate_uuid = uuid.UUID(candidate_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid candidate ID format"
            )
        
        # Get resumes from database
        db_file_service = DBFileService(db)
        resumes = await db_file_service.get_candidate_resumes(candidate_uuid)
        
        resumes_data = []
        for resume in resumes:
            resumes_data.append({
                "id": str(resume.id),
                "file_url": resume.file_url,
                "file_name": resume.file_name,
                "file_size": resume.file_size,
                "file_type": resume.file_type,
                "version": resume.version,
                "is_primary": resume.is_primary,
                "uploaded_at": resume.uploaded_at.isoformat(),
                "is_parsed": resume.is_parsed
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": {
                    "candidate_id": candidate_id,
                    "total_resumes": len(resumes_data),
                    "resumes": resumes_data
                }
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get candidate resumes: {str(e)}"
        )


@router.put("/resume/{resume_id}/primary")
async def set_primary_resume(
    resume_id: str,
    current_user: User = Depends(check_admin_permissions),
    db: AsyncSession = Depends(get_db)
):
    """
    Set a resume as primary (Admin only)
    
    - **resume_id**: Resume ID (UUID) to set as primary
    """
    try:
        # Validate resume_id is a valid UUID
        try:
            resume_uuid = uuid.UUID(resume_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid resume ID format"
            )
        
        # Set as primary using database service
        db_file_service = DBFileService(db)
        resume = await db_file_service.set_primary_resume(resume_uuid)
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Resume set as primary successfully",
                "data": {
                    "id": str(resume.id),
                    "is_primary": resume.is_primary
                }
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set primary resume: {str(e)}"
        )


@router.get("/storage/config")
async def get_storage_config(
    current_user: User = Depends(check_admin_permissions)
):
    """
    Get storage configuration (Admin only)
    """
    try:
        # Get storage config
        config = file_upload_service.get_storage_config()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": config
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get storage config: {str(e)}"
        )


@router.post("/validate")
@rate_limit_public
async def validate_file(
    file: UploadFile = File(..., description="File to validate"),
    file_category: str = Form("general", description="File category for validation rules"),
    max_size_mb: int = Form(10, description="Maximum file size in MB")
):
    """
    Validate file without uploading
    
    - **file**: File to validate
    - **file_category**: File category for appropriate validation rules
    - **max_size_mb**: Maximum file size in MB
    """
    try:
        # Determine allowed types based on category
        allowed_types_map = {
            "resume": [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ],
            "job_description": [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ],
            "image": [
                "image/jpeg",
                "image/png",
                "image/gif",
                "image/webp"
            ],
            "general": file_upload_service.get_storage_config()["config"]["allowed_resume_types"] +
                     file_upload_service.get_storage_config()["config"]["allowed_image_types"]
        }
        
        allowed_types = allowed_types_map.get(file_category, allowed_types_map["general"])
        
        # Validate file
        is_valid, error = await file_upload_service.validate_file(
            file, allowed_types, max_size_mb, file_category
        )
        
        # Virus scan (basic)
        is_safe, scan_message = await file_upload_service.scan_file_for_viruses(file)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": {
                    "is_valid": is_valid,
                    "is_safe": is_safe,
                    "validation_error": error if not is_valid else None,
                    "scan_message": scan_message,
                    "file_name": file.filename,
                    "file_size": None,  # Would need to read file to get size
                    "file_type": file.content_type,
                    "allowed_types": allowed_types,
                    "max_size_mb": max_size_mb,
                    "file_category": file_category
                }
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation failed: {str(e)}"
        )


@router.post("/cleanup")
async def cleanup_old_files(
    days_old: int = 30,
    current_user: User = Depends(check_admin_permissions)
):
    """
    Clean up old files (Admin only)
    
    - **days_old**: Delete files older than this many days (default: 30)
    """
    try:
        # Only local storage supports cleanup
        if file_upload_service.storage_type == "local":
            cleanup_result = file_upload_service.service.cleanup_old_files(days_old)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "message": f"Cleaned up {cleanup_result['deleted_files_count']} files",
                    "data": cleanup_result
                }
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "message": "Cloudinary storage cleanup is managed automatically",
                    "data": {
                        "storage_type": "cloudinary",
                        "cleanup_managed": "automatic"
                    }
                }
            )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cleanup failed: {str(e)}"
        )