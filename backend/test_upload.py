#!/usr/bin/env python3
"""
Test script for file upload system
"""

import os
import sys
import asyncio
from io import BytesIO
from fastapi import UploadFile
from app.services.file_upload_service import file_upload_service


class MockUploadFile:
    """Mock UploadFile for testing"""
    
    def __init__(self, filename: str, content: bytes, content_type: str):
        self.filename = filename
        self._content = content
        self.content_type = content_type
        self._position = 0
    
    async def read(self, size: int = -1):
        if size == -1:
            result = self._content[self._position:]
            self._position = len(self._content)
            return result
        else:
            result = self._content[self._position:self._position + size]
            self._position += len(result)
            return result
    
    async def seek(self, offset: int):
        self._position = offset
    
    @property
    def size(self):
        return len(self._content)


async def test_file_upload():
    """Test the file upload system"""
    print("🧪 Testing File Upload System")
    print("=" * 50)
    
    # Test 1: Check storage configuration
    print("\n1. Checking storage configuration...")
    config = file_upload_service.get_storage_config()
    print(f"   Storage Type: {config['storage_type']}")
    print(f"   Using Cloudinary: {config['using_cloudinary']}")
    print(f"   Cloudinary Configured: {config['cloudinary_configured']}")
    
    # Test 2: Validate file
    print("\n2. Testing file validation...")
    test_content = b"Test resume content"
    test_file = MockUploadFile("test_resume.pdf", test_content, "application/pdf")
    
    is_valid, error = await file_upload_service.validate_file(
        test_file,
        ["application/pdf"],
        5,
        "resume"
    )
    print(f"   File Valid: {is_valid}")
    if error:
        print(f"   Error: {error}")
    
    # Test 3: Virus scan
    print("\n3. Testing virus scan...")
    await test_file.seek(0)
    is_safe, scan_message = await file_upload_service.scan_file_for_viruses(test_file)
    print(f"   File Safe: {is_safe}")
    print(f"   Scan Message: {scan_message}")
    
    # Test 4: Storage usage
    print("\n4. Checking storage usage...")
    try:
        usage = file_upload_service.get_storage_usage()
        print(f"   Total Files: {usage.get('files_count', 'N/A')}")
        print(f"   Used Storage: {usage.get('used_bytes', 'N/A'):,} bytes")
    except Exception as e:
        print(f"   Error getting usage: {e}")
    
    # Test 5: Create test directories for local storage
    print("\n5. Setting up test directories...")
    if config['storage_type'] == 'local':
        test_dirs = [
            "app/static/uploads/resumes",
            "app/static/uploads/job_descriptions", 
            "app/static/uploads/blog_images",
            "app/static/uploads/general"
        ]
        for directory in test_dirs:
            os.makedirs(directory, exist_ok=True)
            print(f"   Created: {directory}")
    
    print("\n" + "=" * 50)
    print("✅ File upload system test completed!")
    
    # Show next steps
    print("\n📋 Next steps for testing:")
    print("   1. Start the FastAPI server: uvicorn app.main:app --reload")
    print("   2. Access API docs: http://localhost:8000/docs")
    print("   3. Test upload endpoints with real files")
    print("   4. Configure Cloudinary in .env file for production use")


if __name__ == "__main__":
    # Add project root to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Run tests
    asyncio.run(test_file_upload())