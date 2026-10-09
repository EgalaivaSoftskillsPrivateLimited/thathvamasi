"""
Local file storage service (fallback when Cloudinary is not available)
"""

import os
import shutil
import uuid
from typing import Optional, Dict, Any, Tuple
from fastapi import UploadFile, HTTPException
from datetime import datetime
import magic
from pathlib import Path
from app.core.config import settings
from app.utils.helpers import sanitize_filename, generate_resume_filename


class LocalStorageService:
    """
    Service for handling local file storage (fallback option)
    """
    
    def __init__(self):
        """Initialize local storage directories"""
        self.base_dir = "app/static/uploads"
        self.resumes_dir = os.path.join(self.base_dir, "resumes")
        self.jds_dir = os.path.join(self.base_dir, "job_descriptions")
        self.blog_images_dir = os.path.join(self.base_dir, "blog_images")
        self.general_dir = os.path.join(self.base_dir, "general")
        
        # Create directories if they don't exist
        for directory in [self.resumes_dir, self.jds_dir, self.blog_images_dir, self.general_dir]:
            os.makedirs(directory, exist_ok=True)
    
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
    
    async def save_file(
        self,
        file: UploadFile,
        directory: str,
        filename: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save file to local storage
        
        Args:
            file: UploadFile object
            directory: Target directory
            filename: Target filename
            metadata: Additional metadata
            
        Returns:
            Dictionary with file details
        """
        try:
            # Ensure directory exists
            os.makedirs(directory, exist_ok=True)
            
            # Create full path
            file_path = os.path.join(directory, filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Get file stats
            file_size = os.path.getsize(file_path)
            
            # Generate URL (relative to static files)
            relative_path = os.path.relpath(file_path, "app/static")
            url = f"/static/{relative_path}"
            
            return {
                "url": url,
                "file_path": file_path,
                "original_filename": file.filename,
                "saved_filename": filename,
                "file_size": file_size,
                "file_type": file.content_type,
                "uploaded_at": datetime.utcnow().isoformat(),
                "metadata": metadata or {}
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    async def upload_resume(
        self,
        file: UploadFile,
        candidate_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload resume file to local storage
        
        Args:
            file: Resume file (PDF, DOC, DOCX)
            candidate_name: Candidate name for filename generation
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload details
        """
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
        
        # Save file
        return await self.save_file(file, self.resumes_dir, filename, metadata)
    
    async def upload_job_description(
        self,
        file: UploadFile,
        company_name: str,
        position_title: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload job description file to local storage
        
        Args:
            file: JD file (PDF, DOC, DOCX)
            company_name: Company name
            position_title: Job position title
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload details
        """
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
        
        # Save file
        return await self.save_file(file, self.jds_dir, filename, metadata)
    
    async def upload_blog_image(
        self,
        file: UploadFile,
        blog_title: str,
        is_featured: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload blog image to local storage
        
        Args:
            file: Image file (JPEG, PNG, GIF, WebP)
            blog_title: Blog title for context
            is_featured: Whether this is a featured image
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload details
        """
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
        safe_title = sanitize_filename(blog_title[:50])
        image_type = "featured" if is_featured else "content"
        filename = f"blog_{image_type}_{safe_title}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        
        # Save file
        return await self.save_file(file, self.blog_images_dir, filename, metadata)
    
    async def upload_general_file(
        self,
        file: UploadFile,
        category: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload general file to local storage
        
        Args:
            file: Any file
            category: File category
            description: File description
            metadata: Additional metadata
            
        Returns:
            Dictionary with upload details
        """
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
        
        # Create category directory
        category_dir = os.path.join(self.general_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Save file
        return await self.save_file(file, category_dir, filename, metadata)
    
    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from local storage
        
        Args:
            file_path: Path to file
            
        Returns:
            True if deleted successfully
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
    
    async def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get file information
        
        Args:
            file_path: Path to file
            
        Returns:
            File information dictionary
        """
        try:
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail="File not found")
            
            file_stats = os.stat(file_path)
            
            return {
                "file_path": file_path,
                "file_size": file_stats.st_size,
                "created_at": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                "is_file": os.path.isfile(file_path)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")
    
    def get_storage_usage(self) -> Dict[str, Any]:
        """
        Get local storage usage statistics
        
        Returns:
            Storage usage information
        """
        try:
            total_size = 0
            file_count = 0
            by_folder = {}
            
            for root, dirs, files in os.walk(self.base_dir):
                folder_size = 0
                folder_files = 0
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        folder_size += file_size
                        total_size += file_size
                        folder_files += 1
                        file_count += 1
                    except OSError:
                        continue
                
                relative_path = os.path.relpath(root, self.base_dir)
                if relative_path != ".":
                    by_folder[relative_path] = {
                        "size_bytes": folder_size,
                        "file_count": folder_files
                    }
            
            return {
                "total_bytes": total_size,
                "used_bytes": total_size,
                "remaining_bytes": 0,  # Local storage doesn't have limits
                "files_count": file_count,
                "by_folder": by_folder,
                "base_directory": self.base_dir
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get storage usage: {str(e)}")
    
    def cleanup_old_files(self, days_old: int = 30) -> Dict[str, Any]:
        """
        Clean up files older than specified days
        
        Args:
            days_old: Delete files older than this many days
            
        Returns:
            Cleanup statistics
        """
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            deleted_files = []
            deleted_size = 0
            
            for root, dirs, files in os.walk(self.base_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    try:
                        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        if file_mtime < cutoff_date:
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            
                            deleted_files.append(file_path)
                            deleted_size += file_size
                    except (OSError, Exception):
                        continue
            
            return {
                "deleted_files_count": len(deleted_files),
                "deleted_size_bytes": deleted_size,
                "deleted_files": deleted_files[:10],  # Return first 10 for logging
                "cutoff_date": cutoff_date.isoformat()
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")


# Create singleton instance
local_storage_service = LocalStorageService()