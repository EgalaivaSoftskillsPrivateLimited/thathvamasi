"""
Custom exceptions for Thathvamasi HR Consultancy
"""

from typing import Any, Dict, Optional


class BaseAPIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message: str, status_code: int = 400, error_code: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class NotFoundError(BaseAPIError):
    """Resource not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class ValidationError(BaseAPIError):
    """Validation error"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422, error_code="VALIDATION_ERROR")


class AuthenticationError(BaseAPIError):
    """Authentication error"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401, error_code="AUTHENTICATION_ERROR")


class AuthorizationError(BaseAPIError):
    """Authorization error"""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, status_code=403, error_code="AUTHORIZATION_ERROR")


class DatabaseError(BaseAPIError):
    """Database operation error"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=500, error_code="DATABASE_ERROR")


class ServiceError(BaseAPIError):
    """Service error"""
    def __init__(self, message: str = "Service error"):
        super().__init__(message, status_code=500, error_code="SERVICE_ERROR")


class RateLimitError(BaseAPIError):
    """Rate limit exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429, error_code="RATE_LIMIT_EXCEEDED")


class ExternalServiceError(BaseAPIError):
    """External service error"""
    def __init__(self, message: str = "External service error"):
        super().__init__(message, status_code=502, error_code="EXTERNAL_SERVICE_ERROR")


class BusinessLogicError(BaseAPIError):
    """Business logic error"""
    def __init__(self, message: str = "Business logic error"):
        super().__init__(message, status_code=400, error_code="BUSINESS_LOGIC_ERROR")