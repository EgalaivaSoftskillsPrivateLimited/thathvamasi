"""
Unified file upload service that uses Cloudinary (primary) or local storage (fallback)
"""

from typing import Optional, Dict, Any, Tuple
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.services.cloudinary_service import cloudinary_service
from app.services.local_storage_service import local_storage_service


class FileUploadService:
    """
    Unified file upload service
    """
    
    def __init__(self):
        """Initialize upload service"""
        self.use_cloudinary = all([
            settings.CLOUDINARY_CLOUD_NAME,
            settings.CLOUDINARY_API_KEY,
            settings.CLOUDINARY_API_SECRET
        ])
        
        if self.use_cloudinary:
            self.service = cloudinary_service
            self.storage_type = "cloudinary"
        else:
            self.service = local_storage_service
            self.storage_type = "local"
    
    async def upload_resume(
        self,
        file: UploadFile,
        candidate_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload resume file
        
        Args:
            file: Resume file
            candidate_name: Candidate name
            metadata: Additional metadata
            
        Returns:
            Upload details with storage type
        """
        result = await self.service.upload_resume(file, candidate_name, metadata)
        result["storage_type"] = self.storage_type
        return result
    
    async def upload_job_description(
        self,
        file: UploadFile,
        company_name: str,
        position_title: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload job description file
        
        Args:
            file: JD file
            company_name: Company name
            position_title: Job position title
            metadata: Additional metadata
            
        Returns:
            Upload details with storage type
        """
        result = await self.service.upload_job_description(
            file, company_name, position_title, metadata
        )
        result["storage_type"] = self.storage_type
        return result
    
    async def upload_blog_image(
        self,
        file: UploadFile,
        blog_title: str,
        is_featured: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload blog image
        
        Args:
            file: Image file
            blog_title: Blog title
            is_featured: Whether featured image
            metadata: Additional metadata
            
        Returns:
            Upload details with storage type
        """
        result = await self.service.upload_blog_image(
            file, blog_title, is_featured, metadata
        )
        result["storage_type"] = self.storage_type
        return result
    
    async def upload_general_file(
        self,
        file: UploadFile,
        category: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload general file
        
        Args:
            file: Any file
            category: File category
            description: File description
            metadata: Additional metadata
            
        Returns:
            Upload details with storage type
        """
        result = await self.service.upload_general_file(
            file, category, description, metadata
        )
        result["storage_type"] = self.storage_type
        return result
    
    async def delete_file(self, identifier: str, resource_type: str = "raw") -> bool:
        """
        Delete file
        
        Args:
            identifier: File identifier (public_id for Cloudinary, file_path for local)
            resource_type: Resource type (Cloudinary only)
            
        Returns:
            True if deleted successfully
        """
        if self.storage_type == "cloudinary":
            return await self.service.delete_file(identifier, resource_type)
        else:
            return await self.service.delete_file(identifier)
    
    async def get_file_info(self, identifier: str, resource_type: str = "raw") -> Dict[str, Any]:
        """
        Get file information
        
        Args:
            identifier: File identifier
            resource_type: Resource type (Cloudinary only)
            
        Returns:
            File information
        """
        if self.storage_type == "cloudinary":
            result = await self.service.get_file_info(identifier, resource_type)
        else:
            result = await self.service.get_file_info(identifier)
        
        result["storage_type"] = self.storage_type
        return result
    
    def get_storage_usage(self) -> Dict[str, Any]:
        """
        Get storage usage statistics
        
        Returns:
            Storage usage information
        """
        result = self.service.get_storage_usage()
        result["storage_type"] = self.storage_type
        result["using_cloudinary"] = self.use_cloudinary
        return result
    
    async def validate_file(
        self,
        file: UploadFile,
        allowed_types: list,
        max_size_mb: int,
        file_category: str = "general"
    ) -> Tuple[bool, str]:
        """
        Validate file
        
        Args:
            file: UploadFile object
            allowed_types: Allowed MIME types
            max_size_mb: Maximum size in MB
            file_category: Category for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        return await self.service.validate_file(file, allowed_types, max_size_mb, file_category)
    
    async def scan_file_for_viruses(self, file: UploadFile) -> Tuple[bool, str]:
        """
        Scan file for viruses
        
        Args:
            file: File to scan
            
        Returns:
            Tuple of (is_safe, message)
        """
        if hasattr(self.service, 'scan_file_for_viruses'):
            return await self.service.scan_file_for_viruses(file)
        
        # Basic validation for local storage
        content = await file.read(1024)
        
        # Check for executable signatures
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
    
    def get_storage_config(self) -> Dict[str, Any]:
        """
        Get storage configuration
        
        Returns:
            Storage configuration
        """
        return {
            "storage_type": self.storage_type,
            "using_cloudinary": self.use_cloudinary,
            "cloudinary_configured": bool(
                settings.CLOUDINARY_CLOUD_NAME and
                settings.CLOUDINARY_API_KEY and
                settings.CLOUDINARY_API_SECRET
            ),
            "config": {
                "max_resume_size_mb": 5,
                "max_jd_size_mb": 10,
                "max_image_size_mb": 5,
                "allowed_resume_types": [
                    "application/pdf",
                    "application/msword",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ],
                "allowed_image_types": [
                    "image/jpeg",
                    "image/png",
                    "image/gif",
                    "image/webp"
                ]
            }
        }
    
    def generate_optimized_image_url(
        self,
        public_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: str = "fill",
        quality: str = "auto",
        format: str = "auto"
    ) -> Optional[str]:
        """
        Generate optimized image URL (Cloudinary only)
        
        Args:
            public_id: Cloudinary public ID
            width: Desired width
            height: Desired height
            crop: Crop mode
            quality: Image quality
            format: Output format
            
        Returns:
            Optimized image URL or None if not using Cloudinary
        """
        if self.storage_type == "cloudinary" and hasattr(self.service, 'generate_image_url'):
            return self.service.generate_image_url(
                public_id, width, height, crop, quality, format
            )
        return None


# Create singleton instance
file_upload_service = FileUploadService()