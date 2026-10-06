"""
Error handling middleware for Thathvamasi HR Consultancy
"""

import logging
import traceback
from typing import Callable, Dict, Any

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import (
    BaseAPIError, NotFoundError, ValidationError, AuthenticationError,
    AuthorizationError, DatabaseError, ServiceError, RateLimitError,
    ExternalServiceError, BusinessLogicError
)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling errors globally
    """
    
    def __init__(self, app, debug: bool = False):
        super().__init__(app)
        self.debug = debug
        self.logger = logging.getLogger(__name__)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Dispatch request with error handling
        """
        try:
            return await call_next(request)
        
        except NotFoundError as e:
            return self._handle_api_error(e, 404)
        
        except ValidationError as e:
            return self._handle_api_error(e, 422)
        
        except AuthenticationError as e:
            return self._handle_api_error(e, 401)
        
        except AuthorizationError as e:
            return self._handle_api_error(e, 403)
        
        except RateLimitError as e:
            return self._handle_api_error(e, 429)
        
        except BusinessLogicError as e:
            return self._handle_api_error(e, 400)
        
        except (DatabaseError, ServiceError) as e:
            self.logger.error(f"Service error: {str(e)}", exc_info=True)
            return self._handle_api_error(e, 500)
        
        except ExternalServiceError as e:
            self.logger.error(f"External service error: {str(e)}", exc_info=True)
            return self._handle_api_error(e, 502)
        
        except BaseAPIError as e:
            return self._handle_api_error(e, e.status_code)
        
        except Exception as e:
            self.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return self._handle_unexpected_error(e)
    
    def _handle_api_error(self, error: BaseAPIError, status_code: int) -> JSONResponse:
        """
        Handle API errors
        """
        error_response = {
            "detail": error.message,
            "error_code": error.error_code or "UNKNOWN_ERROR"
        }
        
        if self.debug:
            error_response["debug"] = {
                "type": error.__class__.__name__,
                "traceback": traceback.format_exc()
            }
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )
    
    def _handle_unexpected_error(self, error: Exception) -> JSONResponse:
        """
        Handle unexpected errors
        """
        error_response = {
            "detail": "An unexpected error occurred. Please try again later.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
        
        if self.debug:
            error_response["debug"] = {
                "type": error.__class__.__name__,
                "message": str(error),
                "traceback": traceback.format_exc()
            }
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for validating requests
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Dispatch request with validation
        """
        # Log incoming request
        self.logger.info(f"Incoming request: {request.method} {request.url.path}")
        
        # Validate request size for file uploads
        if request.method == "POST" and "upload" in request.url.path:
            content_length = request.headers.get("content-length")
            if content_length:
                file_size = int(content_length)
                if file_size > 100 * 1024 * 1024:  # 100MB limit
                    return JSONResponse(
                        status_code=413,
                        content={
                            "detail": "File size exceeds maximum limit of 100MB",
                            "error_code": "FILE_TOO_LARGE"
                        }
                    )
        
        try:
            response = await call_next(request)
            
            # Log response
            self.logger.info(f"Response: {request.method} {request.url.path} - {response.status_code}")
            
            return response
        
        except Exception as e:
            self.logger.error(f"Request validation error: {str(e)}", exc_info=True)
            raise


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """
    Basic rate limiting middleware
    """
    
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_counts: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(__name__)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Dispatch request with rate limiting
        """
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Skip rate limiting for health checks
        if request.url.path.endswith("/health"):
            return await call_next(request)
        
        # Check rate limit
        current_time = time.time()
        client_data = self.request_counts.get(client_ip, {})
        
        if not client_data or current_time - client_data.get("start_time", 0) > self.window_seconds:
            # Reset counter for new window
            self.request_counts[client_ip] = {
                "count": 1,
                "start_time": current_time
            }
        else:
            client_data["count"] += 1
            self.request_counts[client_ip] = client_data
            
            if client_data["count"] > self.max_requests:
                self.logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"Rate limit exceeded. Maximum {self.max_requests} requests per {self.window_seconds} seconds",
                        "error_code": "RATE_LIMIT_EXCEEDED",
                        "retry_after": self.window_seconds
                    },
                    headers={"Retry-After": str(self.window_seconds)}
                )
        
        return await call_next(request)


# Import time for rate limiting
import time