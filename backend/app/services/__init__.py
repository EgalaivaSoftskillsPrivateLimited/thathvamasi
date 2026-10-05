"""
Services package for Thathvamasi HR Consultancy
"""

from app.services.cloudinary_service import CloudinaryService, cloudinary_service
from app.services.local_storage_service import LocalStorageService, local_storage_service
from app.services.file_upload_service import FileUploadService, file_upload_service

__all__ = [
    'CloudinaryService',
    'cloudinary_service',
    'LocalStorageService',
    'local_storage_service',
    'FileUploadService',
    'file_upload_service',
]