"""
Validation utilities for Thathvamasi HR Consultancy
"""

import re
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import ValidationError, BaseModel
from email_validator import validate_email, EmailNotValidError

from app.core.exceptions import ValidationError as AppValidationError


class ValidationUtils:
    """
    Utility class for common validation operations
    """
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """
        Validate phone number (Indian format)
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not phone:
            return False
        
        # Remove all non-digit characters
        cleaned = re.sub(r'\D', '', phone)
        
        # Indian phone numbers should be 10 digits
        # Optional country code (+91) should make it 12-13 digits
        if len(cleaned) == 10:
            # Check if it starts with 6-9 (Indian mobile numbers)
            return cleaned[0] in '6789'
        elif len(cleaned) == 12 and cleaned.startswith('91'):
            # With country code
            return cleaned[2] in '6789'
        elif len(cleaned) == 13 and cleaned.startswith('091'):
            # With 0 prefix
            return cleaned[3] in '6789'
        
        return False
    
    @staticmethod
    def validate_pincode(pincode: str) -> bool:
        """
        Validate Indian pincode
        
        Args:
            pincode: Pincode to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not pincode:
            return False
        
        # Indian pincodes are 6 digits
        return bool(re.match(r'^[1-9][0-9]{5}$', pincode))
    
    @staticmethod
    def validate_date_range(start_date: date, end_date: Optional[date] = None) -> bool:
        """
        Validate date range
        
        Args:
            start_date: Start date
            end_date: End date (optional)
            
        Returns:
            True if valid (end_date > start_date when both provided)
        """
        if end_date and end_date < start_date:
            return False
        return True
    
    @staticmethod
    def validate_age(date_of_birth: date, min_age: int = 18, max_age: int = 65) -> bool:
        """
        Validate age based on date of birth
        
        Args:
            date_of_birth: Date of birth
            min_age: Minimum allowed age
            max_age: Maximum allowed age
            
        Returns:
            True if age is within limits
        """
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return min_age <= age <= max_age
    
    @staticmethod
    def validate_salary(salary: float, min_salary: float = 0, max_salary: float = 100000000) -> bool:
        """
        Validate salary amount
        
        Args:
            salary: Salary amount
            min_salary: Minimum allowed salary
            max_salary: Maximum allowed salary
            
        Returns:
            True if salary is within limits
        """
        return min_salary <= salary <= max_salary
    
    @staticmethod
    def validate_experience(years: float, min_years: float = 0, max_years: float = 50) -> bool:
        """
        Validate years of experience
        
        Args:
            years: Years of experience
            min_years: Minimum allowed experience
            max_years: Maximum allowed experience
            
        Returns:
            True if experience is within limits
        """
        return min_years <= years <= max_years
    
    @staticmethod
    def validate_file_size(file_size: int, max_size_mb: int) -> bool:
        """
        Validate file size
        
        Args:
            file_size: File size in bytes
            max_size_mb: Maximum size in MB
            
        Returns:
            True if file size is within limit
        """
        max_bytes = max_size_mb * 1024 * 1024
        return file_size <= max_bytes
    
    @staticmethod
    def validate_file_type(file_type: str, allowed_types: List[str]) -> bool:
        """
        Validate file type
        
        Args:
            file_type: File MIME type
            allowed_types: List of allowed MIME types
            
        Returns:
            True if file type is allowed
        """
        return file_type.lower() in [t.lower() for t in allowed_types]
    
    @staticmethod
    def validate_skills(skills: List[str], max_skills: int = 20) -> bool:
        """
        Validate skills list
        
        Args:
            skills: List of skills
            max_skills: Maximum number of skills allowed
            
        Returns:
            True if skills list is valid
        """
        if not skills:
            return True
        
        if len(skills) > max_skills:
            return False
        
        # Check each skill is not too long
        for skill in skills:
            if len(skill) > 100:
                return False
        
        return True
    
    @staticmethod
    def validate_tags(tags: List[str], max_tags: int = 10) -> bool:
        """
        Validate tags list
        
        Args:
            tags: List of tags
            max_tags: Maximum number of tags allowed
            
        Returns:
            True if tags list is valid
        """
        if not tags:
            return True
        
        if len(tags) > max_tags:
            return False
        
        # Check each tag is not too long
        for tag in tags:
            if len(tag) > 50:
                return False
        
        return True


class ValidationMiddleware:
    """
    Middleware for request validation
    """
    
    @staticmethod
    def validate_request_data(model_class: BaseModel, data: Dict[str, Any]) -> Optional[AppValidationError]:
        """
        Validate request data against Pydantic model
        
        Args:
            model_class: Pydantic model class
            data: Request data to validate
            
        Returns:
            ValidationError if validation fails, None otherwise
        """
        try:
            model_class(**data)
            return None
        except ValidationError as e:
            error_messages = []
            for error in e.errors():
                field = " -> ".join([str(loc) for loc in error['loc']])
                error_messages.append(f"{field}: {error['msg']}")
            
            error_message = "; ".join(error_messages)
            return AppValidationError(f"Validation failed: {error_message}")


class BusinessRulesValidator:
    """
    Validator for business rules
    """
    
    @staticmethod
    def validate_candidate_registration(candidate_data: Dict[str, Any]) -> Optional[AppValidationError]:
        """
        Validate candidate registration business rules
        
        Args:
            candidate_data: Candidate registration data
            
        Returns:
            ValidationError if business rules are violated, None otherwise
        """
        errors = []
        
        # Check consent
        if not candidate_data.get('consent_accepted'):
            errors.append("Candidate must accept consent to register")
        
        # Check personal details
        personal_details = candidate_data.get('personal_details', {})
        if not personal_details.get('full_name'):
            errors.append("Full name is required")
        
        # Check professional details
        professional_details = candidate_data.get('professional_details', {})
        if not professional_details.get('highest_qualification'):
            errors.append("Highest qualification is required")
        
        if not professional_details.get('total_experience'):
            errors.append("Total experience is required")
        
        # Check notice period if currently employed
        if professional_details.get('current_company') and not professional_details.get('notice_period'):
            errors.append("Notice period is required when currently employed")
        
        if errors:
            return AppValidationError("; ".join(errors))
        
        return None
    
    @staticmethod
    def validate_resume_upload(candidate_id: UUID, file_info: Dict[str, Any]) -> Optional[AppValidationError]:
        """
        Validate resume upload business rules
        
        Args:
            candidate_id: Candidate ID
            file_info: File upload information
            
        Returns:
            ValidationError if business rules are violated, None otherwise
        """
        errors = []
        
        # Check file size
        file_size = file_info.get('file_size', 0)
        if file_size > 5 * 1024 * 1024:  # 5MB
            errors.append("Resume file size must be less than 5MB")
        
        # Check file type
        allowed_types = ['application/pdf', 'application/msword', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        file_type = file_info.get('file_type', '')
        if file_type not in allowed_types:
            errors.append(f"Resume must be PDF, DOC, or DOCX. Got: {file_type}")
        
        # Check file name
        file_name = file_info.get('file_name', '')
        if not file_name:
            errors.append("File name is required")
        elif len(file_name) > 255:
            errors.append("File name is too long (max 255 characters)")
        
        if errors:
            return AppValidationError("; ".join(errors))
        
        return None
    
    @staticmethod
    def validate_status_transition(current_status: str, new_status: str) -> Optional[AppValidationError]:
        """
        Validate candidate status transition
        
        Args:
            current_status: Current status
            new_status: New status
            
        Returns:
            ValidationError if transition is not allowed, None otherwise
        """
        valid_transitions = {
            "new": ["contacted"],
            "contacted": ["shortlisted", "rejected"],
            "shortlisted": ["hired", "rejected"],
            "rejected": ["contacted"],  # Reconsideration
            "hired": [],  # Final state
            "on_hold": ["contacted", "rejected"]
        }
        
        allowed = valid_transitions.get(current_status, [])
        
        if new_status not in allowed:
            return AppValidationError(
                f"Cannot transition from {current_status} to {new_status}. "
                f"Valid transitions: {', '.join(allowed) if allowed else 'none'}"
            )
        
        return None
    
    @staticmethod
    def validate_assignment(candidate_id: UUID, assigned_to: UUID) -> Optional[AppValidationError]:
        """
        Validate candidate assignment
        
        Args:
            candidate_id: Candidate ID
            assigned_to: User ID to assign to
            
        Returns:
            ValidationError if assignment is not valid, None otherwise
        """
        # In a real application, you would check:
        # 1. assigned_to is a valid user ID
        # 2. User has permission to handle candidates
        # 3. User is not already overloaded with candidates
        # 4. User's expertise matches candidate's profile
        
        # For now, just validate that assigned_to is not None
        if not assigned_to:
            return AppValidationError("Assigned user ID is required")
        
        return None


# Create singleton instances
validation_utils = ValidationUtils()
validation_middleware = ValidationMiddleware()
business_rules_validator = BusinessRulesValidator()