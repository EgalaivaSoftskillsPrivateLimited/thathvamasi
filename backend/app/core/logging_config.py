"""
Logging configuration for Thathvamasi HR Consultancy
"""

import logging
import sys
from typing import Optional
from pathlib import Path

from app.core.config import settings


def setup_logging(log_level: Optional[str] = None):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if log_level is None:
        log_level = settings.LOG_LEVEL
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configure handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    handlers.append(console_handler)
    
    # File handler for errors
    error_handler = logging.FileHandler("logs/error.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format, date_format))
    handlers.append(error_handler)
    
    # File handler for all logs (rotating)
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    handlers.append(file_handler)
    
    # Setup root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )
    
    # Set specific log levels for libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {log_level}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Log files will be saved in: {log_dir.absolute()}")


class RequestLogger:
    """
    Logger for HTTP requests
    """
    
    def __init__(self):
        self.logger = logging.getLogger("request")
    
    def log_request(self, request_info: dict):
        """
        Log HTTP request
        
        Args:
            request_info: Dictionary with request information
        """
        self.logger.info(
            f"Request: {request_info.get('method')} {request_info.get('path')} "
            f"from {request_info.get('client_ip')} - "
            f"Status: {request_info.get('status_code')} "
            f"Duration: {request_info.get('duration_ms', 0)}ms"
        )
    
    def log_error(self, request_info: dict, error: Exception):
        """
        Log request error
        
        Args:
            request_info: Dictionary with request information
            error: Exception that occurred
        """
        self.logger.error(
            f"Error in {request_info.get('method')} {request_info.get('path')} "
            f"from {request_info.get('client_ip')}: {str(error)}",
            exc_info=True
        )
    
    def log_slow_request(self, request_info: dict, threshold_ms: int = 1000):
        """
        Log slow requests
        
        Args:
            request_info: Dictionary with request information
            threshold_ms: Threshold in milliseconds for slow requests
        """
        duration = request_info.get('duration_ms', 0)
        if duration > threshold_ms:
            self.logger.warning(
                f"Slow request: {request_info.get('method')} {request_info.get('path')} "
                f"took {duration}ms (threshold: {threshold_ms}ms)"
            )


class DatabaseLogger:
    """
    Logger for database operations
    """
    
    def __init__(self):
        self.logger = logging.getLogger("database")
    
    def log_query(self, query: str, params: dict, duration_ms: float):
        """
        Log database query
        
        Args:
            query: SQL query
            params: Query parameters
            duration_ms: Query duration in milliseconds
        """
        if duration_ms > 100:  # Log slow queries (>100ms)
            self.logger.warning(
                f"Slow query ({duration_ms}ms): {query[:200]}... "
                f"Params: {params}"
            )
    
    def log_connection(self, action: str, details: str = ""):
        """
        Log database connection events
        
        Args:
            action: Connection action (connect, disconnect, pool)
            details: Additional details
        """
        self.logger.info(f"Database {action}: {details}")
    
    def log_error(self, error: Exception, context: str = ""):
        """
        Log database error
        
        Args:
            error: Database error
            context: Error context
        """
        self.logger.error(f"Database error {context}: {str(error)}", exc_info=True)


class FileUploadLogger:
    """
    Logger for file upload operations
    """
    
    def __init__(self):
        self.logger = logging.getLogger("file_upload")
    
    def log_upload(self, file_info: dict, success: bool, duration_ms: float):
        """
        Log file upload
        
        Args:
            file_info: File information dictionary
            success: Whether upload was successful
            duration_ms: Upload duration in milliseconds
        """
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"File upload {status}: {file_info.get('file_name')} "
            f"({file_info.get('file_size', 0)} bytes) "
            f"to {file_info.get('storage_type', 'unknown')} "
            f"in {duration_ms}ms"
        )
    
    def log_security_check(self, file_info: dict, is_safe: bool, check_type: str):
        """
        Log security check results
        
        Args:
            file_info: File information dictionary
            is_safe: Whether file passed security check
            check_type: Type of security check (virus, type, size)
        """
        status = "PASSED" if is_safe else "FAILED"
        self.logger.info(
            f"Security check {check_type} {status} for {file_info.get('file_name')}"
        )
    
    def log_error(self, error: Exception, file_info: dict):
        """
        Log file upload error
        
        Args:
            error: Upload error
            file_info: File information dictionary
        """
        self.logger.error(
            f"File upload error for {file_info.get('file_name', 'unknown')}: {str(error)}",
            exc_info=True
        )


# Create singleton instances
request_logger = RequestLogger()
database_logger = DatabaseLogger()
file_upload_logger = FileUploadLogger()