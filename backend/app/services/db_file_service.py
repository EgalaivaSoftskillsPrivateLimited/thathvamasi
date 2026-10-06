"""
Database service for managing file metadata in PostgreSQL
"""

import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.user_model import User
from app.models.candidate_model import CandidateResume
from app.models.client_model import JobDescriptionDocument, ClientDocument
from app.models.blog_model import BlogImage
from app.services.file_upload_service import file_upload_service


class DBFileService:
    """
    Service for managing file metadata in PostgreSQL database
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def save_resume_metadata(
        self,
        candidate_id: uuid.UUID,
        upload_result: Dict[str, Any],
        is_primary: bool = True,
        uploaded_by: Optional[str] = None
    ) -> CandidateResume:
        """
        Save resume metadata to database
        
        Args:
            candidate_id: Candidate ID
            upload_result: Result from file upload service
            is_primary: Whether this is the primary resume
            uploaded_by: Who uploaded the resume
            
        Returns:
            CandidateResume object
        """
        try:
            # If there's an existing primary resume, mark it as non-primary
            if is_primary:
                stmt = select(CandidateResume).where(
                    CandidateResume.candidate_id == candidate_id,
                    CandidateResume.is_primary == True
                )
                result = await self.db.execute(stmt)
                existing_primary = result.scalar_one_or_none()
                
                if existing_primary:
                    existing_primary.is_primary = False
            
            # Get the latest version number
            stmt = select(CandidateResume).where(
                CandidateResume.candidate_id == candidate_id
            ).order_by(CandidateResume.version.desc())
            result = await self.db.execute(stmt)
            latest_resume = result.scalar_one_or_none()
            
            version = latest_resume.version + 1 if latest_resume else 1
            
            # Create new resume record
            resume = CandidateResume(
                id=uuid.uuid4(),
                candidate_id=candidate_id,
                file_url=upload_result["url"],
                file_name=upload_result.get("original_filename", upload_result.get("file_name", "")),
                file_size=upload_result["file_size"],
                file_type=upload_result["file_type"],
                cloudinary_id=upload_result.get("public_id"),
                version=version,
                is_primary=is_primary,
                uploaded_by=uploaded_by,
                is_parsed=False,
                parsed_data=None
            )
            
            self.db.add(resume)
            await self.db.commit()
            await self.db.refresh(resume)
            
            return resume
            
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def save_jd_metadata(
        self,
        hiring_requirement_id: uuid.UUID,
        upload_result: Dict[str, Any],
        is_primary: bool = True,
        uploaded_by: Optional[str] = None
    ) -> JobDescriptionDocument:
        """
        Save job description metadata to database
        
        Args:
            hiring_requirement_id: Hiring requirement ID
            upload_result: Result from file upload service
            is_primary: Whether this is the primary JD
            uploaded_by: Who uploaded the JD
            
        Returns:
            JobDescriptionDocument object
        """
        try:
            # If there's an existing primary JD, mark it as non-primary
            if is_primary:
                stmt = select(JobDescriptionDocument).where(
                    JobDescriptionDocument.hiring_requirement_id == hiring_requirement_id,
                    JobDescriptionDocument.is_primary == True
                )
                result = await self.db.execute(stmt)
                existing_primary = result.scalar_one_or_none()
                
                if existing_primary:
                    existing_primary.is_primary = False
            
            # Get the latest version number
            stmt = select(JobDescriptionDocument).where(
                JobDescriptionDocument.hiring_requirement_id == hiring_requirement_id
            ).order_by(JobDescriptionDocument.version.desc())
            result = await self.db.execute(stmt)
            latest_jd = result.scalar_one_or_none()
            
            version = latest_jd.version + 1 if latest_jd else 1
            
            # Create new JD record
            jd = JobDescriptionDocument(
                id=uuid.uuid4(),
                hiring_requirement_id=hiring_requirement_id,
                file_url=upload_result["url"],
                file_name=upload_result.get("original_filename", upload_result.get("file_name", "")),
                file_size=upload_result["file_size"],
                file_type=upload_result["file_type"],
                cloudinary_id=upload_result.get("public_id"),
                version=version,
                is_primary=is_primary,
                uploaded_by=uploaded_by,
                is_parsed=False,
                parsed_data=None
            )
            
            self.db.add(jd)
            await self.db.commit()
            await self.db.refresh(jd)
            
            return jd
            
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def save_client_document_metadata(
        self,
        client_id: uuid.UUID,
        document_type: str,
        title: str,
        upload_result: Dict[str, Any],
        description: Optional[str] = None,
        status: str = "draft",
        uploaded_by: Optional[uuid.UUID] = None
    ) -> ClientDocument:
        """
        Save client document metadata to database
        
        Args:
            client_id: Client ID
            document_type: Type of document
            title: Document title
            upload_result: Result from file upload service
            description: Document description
            status: Document status
            uploaded_by: User ID who uploaded
            
        Returns:
            ClientDocument object
        """
        try:
            # Get the latest version for this document type and title
            stmt = select(ClientDocument).where(
                ClientDocument.client_id == client_id,
                ClientDocument.document_type == document_type,
                ClientDocument.title == title
            ).order_by(ClientDocument.version.desc())
            result = await self.db.execute(stmt)
            latest_doc = result.scalar_one_or_none()
            
            version = latest_doc.version + 1 if latest_doc else 1
            
            # Create new document record
            doc = ClientDocument(
                id=uuid.uuid4(),
                client_id=client_id,
                document_type=document_type,
                title=title,
                description=description,
                file_url=upload_result["url"],
                file_name=upload_result.get("original_filename", upload_result.get("file_name", "")),
                file_size=upload_result["file_size"],
                file_type=upload_result["file_type"],
                cloudinary_id=upload_result.get("public_id"),
                status=status,
                version=version,
                uploaded_by=uploaded_by
            )
            
            self.db.add(doc)
            await self.db.commit()
            await self.db.refresh(doc)
            
            return doc
            
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def save_blog_image_metadata(
        self,
        blog_id: uuid.UUID,
        upload_result: Dict[str, Any],
        alt_text: Optional[str] = None,
        caption: Optional[str] = None,
        is_featured: bool = False,
        uploaded_by: Optional[str] = None
    ) -> BlogImage:
        """
        Save blog image metadata to database
        
        Args:
            blog_id: Blog ID
            upload_result: Result from file upload service
            alt_text: Image alt text
            caption: Image caption
            is_featured: Whether this is a featured image
            uploaded_by: Who uploaded the image
            
        Returns:
            BlogImage object
        """
        try:
            # If this is a featured image and there's an existing featured image,
            # mark it as non-featured
            if is_featured:
                stmt = select(BlogImage).where(
                    BlogImage.blog_id == blog_id,
                    BlogImage.is_featured == True
                )
                result = await self.db.execute(stmt)
                existing_featured = result.scalar_one_or_none()
                
                if existing_featured:
                    existing_featured.is_featured = False
            
            # Create new image record
            image = BlogImage(
                id=uuid.uuid4(),
                blog_id=blog_id,
                image_url=upload_result["url"],
                thumbnail_url=upload_result.get("thumbnail_url"),
                original_filename=upload_result.get("original_filename", upload_result.get("file_name", "")),
                file_size=upload_result["file_size"],
                file_type=upload_result["file_type"],
                width=upload_result.get("width"),
                height=upload_result.get("height"),
                cloudinary_id=upload_result.get("public_id"),
                alt_text=alt_text,
                caption=caption,
                is_featured=is_featured,
                uploaded_by=uploaded_by
            )
            
            self.db.add(image)
            await self.db.commit()
            await self.db.refresh(image)
            
            return image
            
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def get_resume(self, resume_id: uuid.UUID) -> Optional[CandidateResume]:
        """
        Get resume by ID
        
        Args:
            resume_id: Resume ID
            
        Returns:
            CandidateResume object or None
        """
        stmt = select(CandidateResume).where(CandidateResume.id == resume_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_candidate_resumes(self, candidate_id: uuid.UUID) -> List[CandidateResume]:
        """
        Get all resumes for a candidate
        
        Args:
            candidate_id: Candidate ID
            
        Returns:
            List of CandidateResume objects
        """
        stmt = select(CandidateResume).where(
            CandidateResume.candidate_id == candidate_id
        ).order_by(CandidateResume.version.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_primary_resume(self, candidate_id: uuid.UUID) -> Optional[CandidateResume]:
        """
        Get primary resume for a candidate
        
        Args:
            candidate_id: Candidate ID
            
        Returns:
            Primary CandidateResume or None
        """
        stmt = select(CandidateResume).where(
            CandidateResume.candidate_id == candidate_id,
            CandidateResume.is_primary == True
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def set_primary_resume(self, resume_id: uuid.UUID) -> Optional[CandidateResume]:
        """
        Set a resume as primary
        
        Args:
            resume_id: Resume ID to set as primary
            
        Returns:
            Updated CandidateResume or None if not found
        """
        try:
            # Get the resume
            stmt = select(CandidateResume).where(CandidateResume.id == resume_id)
            result = await self.db.execute(stmt)
            resume = result.scalar_one_or_none()
            
            if not resume:
                return None
            
            # Get current primary resume
            stmt = select(CandidateResume).where(
                CandidateResume.candidate_id == resume.candidate_id,
                CandidateResume.is_primary == True,
                CandidateResume.id != resume_id
            )
            result = await self.db.execute(stmt)
            current_primary = result.scalar_one_or_none()
            
            # Update resumes
            if current_primary:
                current_primary.is_primary = False
            
            resume.is_primary = True
            
            await self.db.commit()
            await self.db.refresh(resume)
            
            return resume
            
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def delete_resume(self, resume_id: uuid.UUID) -> bool:
        """
        Delete resume from database and storage
        
        Args:
            resume_id: Resume ID
            
        Returns:
            True if deleted successfully
        """
        try:
            # Get the resume
            stmt = select(CandidateResume).where(CandidateResume.id == resume_id)
            result = await self.db.execute(stmt)
            resume = result.scalar_one_or_none()
            
            if not resume:
                return False
            
            # Delete from storage if cloudinary_id exists
            if resume.cloudinary_id and file_upload_service.storage_type == "cloudinary":
                await file_upload_service.delete_file(resume.cloudinary_id, "raw")
            
            # Delete from database
            await self.db.delete(resume)
            await self.db.commit()
            
            return True
            
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def get_jd_document(self, jd_id: uuid.UUID) -> Optional[JobDescriptionDocument]:
        """
        Get JD document by ID
        
        Args:
            jd_id: JD document ID
            
        Returns:
            JobDescriptionDocument object or None
        """
        stmt = select(JobDescriptionDocument).where(JobDescriptionDocument.id == jd_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_hiring_requirement_jds(self, hiring_requirement_id: uuid.UUID) -> List[JobDescriptionDocument]:
        """
        Get all JDs for a hiring requirement
        
        Args:
            hiring_requirement_id: Hiring requirement ID
            
        Returns:
            List of JobDescriptionDocument objects
        """
        stmt = select(JobDescriptionDocument).where(
            JobDescriptionDocument.hiring_requirement_id == hiring_requirement_id
        ).order_by(JobDescriptionDocument.version.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_client_documents(self, client_id: uuid.UUID, document_type: Optional[str] = None) -> List[ClientDocument]:
        """
        Get documents for a client
        
        Args:
            client_id: Client ID
            document_type: Optional document type filter
            
        Returns:
            List of ClientDocument objects
        """
        stmt = select(ClientDocument).where(ClientDocument.client_id == client_id)
        
        if document_type:
            stmt = stmt.where(ClientDocument.document_type == document_type)
        
        stmt = stmt.order_by(ClientDocument.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_blog_images(self, blog_id: uuid.UUID) -> List[BlogImage]:
        """
        Get images for a blog
        
        Args:
            blog_id: Blog ID
            
        Returns:
            List of BlogImage objects
        """
        stmt = select(BlogImage).where(
            BlogImage.blog_id == blog_id
        ).order_by(
            BlogImage.is_featured.desc(),
            BlogImage.created_at.desc()
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def update_resume_parsed_data(self, resume_id: uuid.UUID, parsed_data: Dict[str, Any]) -> Optional[CandidateResume]:
        """
        Update resume parsed data
        
        Args:
            resume_id: Resume ID
            parsed_data: Parsed resume data
            
        Returns:
            Updated CandidateResume or None
        """
        try:
            stmt = select(CandidateResume).where(CandidateResume.id == resume_id)
            result = await self.db.execute(stmt)
            resume = result.scalar_one_or_none()
            
            if not resume:
                return None
            
            resume.is_parsed = True
            resume.parsed_data = parsed_data
            
            await self.db.commit()
            await self.db.refresh(resume)
            
            return resume
            
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def update_jd_parsed_data(self, jd_id: uuid.UUID, parsed_data: Dict[str, Any]) -> Optional[JobDescriptionDocument]:
        """
        Update JD parsed data
        
        Args:
            jd_id: JD document ID
            parsed_data: Parsed JD data
            
        Returns:
            Updated JobDescriptionDocument or None
        """
        try:
            stmt = select(JobDescriptionDocument).where(JobDescriptionDocument.id == jd_id)
            result = await self.db.execute(stmt)
            jd = result.scalar_one_or_none()
            
            if not jd:
                return None
            
            jd.is_parsed = True
            jd.parsed_data = parsed_data
            
            await self.db.commit()
            await self.db.refresh(jd)
            
            return jd
            
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def get_file_stats(self) -> Dict[str, Any]:
        """
        Get file storage statistics
        
        Returns:
            Dictionary with file statistics
        """
        try:
            # Count resumes
            stmt = select(CandidateResume)
            result = await self.db.execute(stmt)
            resume_count = len(result.scalars().all())
            
            # Count JDs
            stmt = select(JobDescriptionDocument)
            result = await self.db.execute(stmt)
            jd_count = len(result.scalars().all())
            
            # Count client documents
            stmt = select(ClientDocument)
            result = await self.db.execute(stmt)
            client_doc_count = len(result.scalars().all())
            
            # Count blog images
            stmt = select(BlogImage)
            result = await self.db.execute(stmt)
            blog_image_count = len(result.scalars().all())
            
            # Total file count
            total_count = resume_count + jd_count + client_doc_count + blog_image_count
            
            return {
                "total_files": total_count,
                "resumes": resume_count,
                "job_descriptions": jd_count,
                "client_documents": client_doc_count,
                "blog_images": blog_image_count,
                "storage_type": file_upload_service.storage_type,
                "using_cloudinary": file_upload_service.use_cloudinary
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "total_files": 0,
                "resumes": 0,
                "job_descriptions": 0,
                "client_documents": 0,
                "blog_images": 0
            }