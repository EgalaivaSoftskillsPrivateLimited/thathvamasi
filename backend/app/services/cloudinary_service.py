"""
Cloudinary service for file uploads and management
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url
from typing import Optional, Tuple, Dict, Any, BinaryIO
from fastapi import UploadFile, HTTPException
import magic
import os
from datetime import datetime
from app.core.config import settings
from app.utils.helpers import generate_resume_filename, sanitize_filename


class CloudinaryService:
    """
    Service for handling Cloudinary file uploads and management
    """
    
    def __init__(self):
        """Initialize Cloudinary configuration"""
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )
    
    async def validate_file(
        self,
        file: UploadFile,
        allowed_types: list,
        max_size_mb: int,
        file_category: str = "general"
    ) -> Tuple[bool, str]:
        """
        Validate file before upload
        
        Args:
            file: UploadFile object
            allowed_types: List of allowed MIME types
            max_size_mb: Maximum file size in MB
            file_category: Category for error messages
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file size
        file_size = 0
        content = await file.read(1024 * 1024 * (max_size_mb + 1))  # Read slightly more than max
        file_size = len(content)
        
        if file_size > max_size_mb * 1024 * 1024:
            return False, f"{file_category} file size exceeds {max_size_mb}MB limit"
        
        # Check file type using magic
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(content)
        
        if file_type not in allowed_types:
            return False, f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        
        # Reset file pointer
        await file.seek(0)
        
        return True, ""
    
    async def upload_resume(
        self,
        file: UploadFile,
        candidate_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload resume file to Cloudinary
        
        Args:
            file: Resume file (PDF, DOC, DOCX)
            candidate_name: Candidate name for filename generation
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload details
        """
        try:
            # Validate file
            allowed_types = [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ]
            
            is_valid, error = await self.validate_file(
                file, allowed_types, max_size_mb=5, file_category="Resume"
            )
            
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            
            # Generate filename
            file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else 'pdf'
            filename = generate_resume_filename(candidate_name, file_extension)
            
            # Read file content
            content = await file.read()
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                content,
                folder=f"{settings.CLOUDINARY_FOLDER}/resumes",
                public_id=filename,
                resource_type="raw",
                overwrite=False,
                tags=["resume", "candidate"],
                context={
                    "caption": f"Resume of {candidate_name}",
                    "original_filename": sanitize_filename(file.filename)
                }
            )
            
            # Generate secure URL
            secure_url, _ = cloudinary_url(
                upload_result['public_id'],
                resource_type="raw",
                secure=True,
                type="upload"
            )
            
            return {
                "url": secure_url,
                "public_id": upload_result['public_id'],
                "original_filename": file.filename,
                "file_size": len(content),
                "file_type": file.content_type,
                "uploaded_at": datetime.utcnow().isoformat(),
                "cloudinary_metadata": {
                    "version": upload_result.get('version'),
                    "format": upload_result.get('format'),
                    "resource_type": upload_result.get('resource_type')
                }
            }
            
        except cloudinary.exceptions.Error as e:
            raise HTTPException(status_code=500, detail=f"Cloudinary upload error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    async def upload_job_description(
        self,
        file: UploadFile,
        company_name: str,
        position_title: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload job description file to Cloudinary
        
        Args:
            file: JD file (PDF, DOC, DOCX)
            company_name: Company name
            position_title: Job position title
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload details
        """
        try:
            # Validate file
            allowed_types = [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ]
            
            is_valid, error = await self.validate_file(
                file, allowed_types, max_size_mb=10, file_category="Job Description"
            )
            
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            
            # Generate filename
            file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else 'pdf'
            safe_company = sanitize_filename(company_name)
            safe_position = sanitize_filename(position_title)
            filename = f"jd_{safe_company}_{safe_position}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
            
            # Read file content
            content = await file.read()
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                content,
                folder=f"{settings.CLOUDINARY_FOLDER}/job_descriptions",
                public_id=filename,
                resource_type="raw",
                overwrite=False,
                tags=["job_description", "jd", "client"],
                context={
                    "caption": f"JD for {position_title} at {company_name}",
                    "original_filename": sanitize_filename(file.filename)
                }
            )
            
            # Generate secure URL
            secure_url, _ = cloudinary_url(
                upload_result['public_id'],
                resource_type="raw",
                secure=True,
                type="upload"
            )
            
            return {
                "url": secure_url,
                "public_id": upload_result['public_id'],
                "original_filename": file.filename,
                "file_size": len(content),
                "file_type": file.content_type,
                "uploaded_at": datetime.utcnow().isoformat(),
                "cloudinary_metadata": {
                    "version": upload_result.get('version'),
                    "format": upload_result.get('format'),
                    "resource_type": upload_result.get('resource_type')
                }
            }
            
        except cloudinary.exceptions.Error as e:
            raise HTTPException(status_code=500, detail=f"Cloudinary upload error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    async def upload_blog_image(
        self,
        file: UploadFile,
        blog_title: str,
        is_featured: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload blog image to Cloudinary with optimization
        
        Args:
            file: Image file (JPEG, PNG, GIF, WebP)
            blog_title: Blog title for context
            is_featured: Whether this is a featured image
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload details
        """
        try:
            # Validate file
            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/gif",
                "image/webp"
            ]
            
            is_valid, error = await self.validate_file(
                file, allowed_types, max_size_mb=5, file_category="Image"
            )
            
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            
            # Generate filename
            file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else 'jpg'
            safe_title = sanitize_filename(blog_title[:50])  # Limit length
            image_type = "featured" if is_featured else "content"
            filename = f"blog_{image_type}_{safe_title}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
            
            # Read file content
            content = await file.read()
            
            # Upload to Cloudinary with optimization
            upload_result = cloudinary.uploader.upload(
                content,
                folder=f"{settings.CLOUDINARY_FOLDER}/blog_images",
                public_id=filename,
                transformation=[
                    {"quality": "auto", "fetch_format": "auto"},
                    {"width": 1200, "crop": "limit"}  # Limit width for featured images
                ] if is_featured else [
                    {"quality": "auto", "fetch_format": "auto"}
                ],
                overwrite=False,
                tags=["blog", "image", image_type],
                context={
                    "caption": f"Blog image: {blog_title}",
                    "alt": blog_title,
                    "original_filename": sanitize_filename(file.filename)
                }
            )
            
            # Generate optimized URLs
            optimized_url, _ = cloudinary_url(
                upload_result['public_id'],
                transformation=[
                    {"quality": "auto", "fetch_format": "auto"}
                ],
                secure=True
            )
            
            # Thumbnail URL for lists
            thumbnail_url, _ = cloudinary_url(
                upload_result['public_id'],
                transformation=[
                    {"width": 300, "height": 200, "crop": "fill"},
                    {"quality": "auto", "fetch_format": "auto"}
                ],
                secure=True
            )
            
            return {
                "url": optimized_url,
                "thumbnail_url": thumbnail_url,
                "public_id": upload_result['public_id'],
                "original_filename": file.filename,
                "file_size": len(content),
                "file_type": file.content_type,
                "width": upload_result.get('width'),
                "height": upload_result.get('height'),
                "format": upload_result.get('format'),
                "uploaded_at": datetime.utcnow().isoformat(),
                "is_featured": is_featured
            }
            
        except cloudinary.exceptions.Error as e:
            raise HTTPException(status_code=500, detail=f"Cloudinary upload error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    async def upload_general_file(
        self,
        file: UploadFile,
        category: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload general file to Cloudinary
        
        Args:
            file: Any file
            category: File category (e.g., 'document', 'image', 'other')
            description: File description
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload details
        """
        try:
            # Basic validation
            is_valid, error = await self.validate_file(
                file, settings.ALLOWED_FILE_TYPES, max_size_mb=10, file_category="File"
            )
            
            if not is_valid:
                raise HTTPException(status_code=400, detail=error)
            
            # Generate filename
            file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else 'bin'
            safe_description = sanitize_filename(description[:50])
            filename = f"{category}_{safe_description}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
            
            # Read file content
            content = await file.read()
            
            # Determine resource type
            resource_type = "auto"
            if file.content_type.startswith("image/"):
                resource_type = "image"
            elif file.content_type.startswith("video/"):
                resource_type = "video"
            elif file.content_type.startswith("application/"):
                resource_type = "raw"
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                content,
                folder=f"{settings.CLOUDINARY_FOLDER}/{category}",
                public_id=filename,
                resource_type=resource_type,
                overwrite=False,
                tags=[category, "upload"],
                context={
                    "description": description,
                    "original_filename": sanitize_filename(file.filename)
                }
            )
            
            # Generate URL
            secure_url, _ = cloudinary_url(
                upload_result['public_id'],
                resource_type=resource_type,
                secure=True,
                type="upload"
            )
            
            return {
                "url": secure_url,
                "public_id": upload_result['public_id'],
                "original_filename": file.filename,
                "file_size": len(content),
                "file_type": file.content_type,
                "resource_type": resource_type,
                "uploaded_at": datetime.utcnow().isoformat(),
                "category": category
            }
            
        except cloudinary.exceptions.Error as e:
            raise HTTPException(status_code=500, detail=f"Cloudinary upload error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    async def delete_file(self, public_id: str, resource_type: str = "raw") -> bool:
        """
        Delete file from Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            resource_type: Resource type (image, raw, video)
            
        Returns:
            True if deleted successfully
        """
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
            return result.get('result') == 'ok'
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
    
    async def get_file_info(self, public_id: str, resource_type: str = "raw") -> Dict[str, Any]:
        """
        Get file information from Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            resource_type: Resource type
            
        Returns:
            File information dictionary
        """
        try:
            result = cloudinary.api.resource(public_id, resource_type=resource_type)
            return result
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
    
    def generate_image_url(
        self,
        public_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: str = "fill",
        quality: str = "auto",
        format: str = "auto"
    ) -> str:
        """
        Generate optimized image URL
        
        Args:
            public_id: Cloudinary public ID
            width: Desired width
            height: Desired height
            crop: Crop mode
            quality: Image quality
            format: Output format
            
        Returns:
            Optimized image URL
        """
        transformation = []
        
        if width or height:
            transformation.append({"width": width, "height": height, "crop": crop})
        
        transformation.append({"quality": quality, "fetch_format": format})
        
        url, _ = cloudinary_url(public_id, transformation=transformation, secure=True)
        return url
    
    async def scan_file_for_viruses(self, file: UploadFile) -> Tuple[bool, str]:
        """
        Scan file for viruses (placeholder - integrate with antivirus service)
        
        Args:
            file: File to scan
            
        Returns:
            Tuple of (is_safe, message)
        """
        # This is a placeholder. In production, integrate with:
        # 1. ClamAV (open source)
        # 2. VirusTotal API
        # 3. Commercial antivirus service
        
        # For now, do basic checks
        content = await file.read(1024)  # Read first KB
        
        # Check for executable signatures (basic)
        executable_signatures = [
            b'MZ',  # Windows EXE
            b'\x7fELF',  # Linux ELF
            b'\xca\xfe\xba\xbe',  # Java class
        ]
        
        for sig in executable_signatures:
            if content.startswith(sig):
                await file.seek(0)
                return False, "File appears to be an executable, which is not allowed"
        
        await file.seek(0)
        return True, "File appears safe (basic scan)"
    
    def get_storage_usage(self) -> Dict[str, Any]:
        """
        Get Cloudinary storage usage statistics
        
        Returns:
            Storage usage information
        """
        try:
            # Note: This requires Cloudinary admin API permissions
            # For now, return placeholder
            return {
                "total_bytes": 0,
                "used_bytes": 0,
                "remaining_bytes": 0,
                "files_count": 0,
                "by_folder": {}
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get storage usage: {str(e)}")


# Create singleton instance
cloudinary_service = CloudinaryService()