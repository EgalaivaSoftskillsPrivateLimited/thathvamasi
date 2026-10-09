"""
Utility functions and helpers
"""

import os
import re
from typing import Any, Dict
from datetime import datetime, date
from uuid import UUID
import json


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing potentially unsafe characters
    """
    clean_name = os.path.basename(filename)
    clean_name = re.sub(r'[^a-zA-Z0-9._-]', '_', clean_name)
    clean_name = re.sub(r'\.{2,}', '.', clean_name)
    return clean_name or "file"


def to_camel_case(snake_str: str) -> str:
    """
    Convert snake_case to camelCase
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(camel_str: str) -> str:
    """
    Convert camelCase to snake_case
    """
    snake_str = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()
    return snake_str


def format_datetime(dt: datetime) -> str:
    """
    Format datetime to ISO string
    """
    return dt.isoformat() if dt else None


def parse_datetime(dt_str: str) -> datetime:
    """
    Parse ISO datetime string
    """
    try:
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except ValueError:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")


def validate_indian_mobile(mobile: str) -> bool:
    """
    Validate Indian mobile number
    Format: +91XXXXXXXXXX or 0XXXXXXXXXX or XXXXXXXXXX
    """
    pattern = r'^(\+91|0)?[6-9]\d{9}$'
    return bool(re.match(pattern, mobile))


def validate_email(email: str) -> bool:
    """
    Validate email address
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """
    Validate file extension
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def calculate_age(birth_date: date) -> int:
    """
    Calculate age from birth date
    """
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def generate_slug(text: str) -> str:
    """
    Generate URL slug from text
    """
    # Convert to lowercase
    slug = text.lower()
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'[\s]+', '-', slug)
    # Remove consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    # Trim hyphens from start and end
    slug = slug.strip('-')
    return slug


def truncate_text(text: str, length: int = 100) -> str:
    """
    Truncate text to specified length
    """
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + '...'


def serialize_object(obj: Any) -> Dict:
    """
    Serialize object for JSON response
    """
    if isinstance(obj, datetime):
        return format_datetime(obj)
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    elif hasattr(obj, 'model_dump'):
        return obj.model_dump()
    elif hasattr(obj, 'dict'):
        return obj.dict()
    elif hasattr(obj, '__dict__'):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
    else:
        return str(obj)


def generate_resume_filename(name: str, extension: str = 'pdf') -> str:
    """
    Generate filename for resume
    Format: FirstName_LastName_YYYYMMDD_HHMMSS.ext
    """
    # Clean name
    clean_name = re.sub(r'[^\w\s]', '', name)
    clean_name = clean_name.replace(' ', '_').lower()
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"{clean_name}_{timestamp}.{extension}"


def format_currency(amount: float) -> str:
    """
    Format currency for Indian Rupees
    """
    if amount >= 10000000:  # 1 Crore
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh
        return f"₹{amount/100000:.2f} L"
    else:
        return f"₹{amount:,.2f}"


def calculate_experience_years(start_date: date, end_date: date = None) -> float:
    """
    Calculate experience in years
    """
    if end_date is None:
        end_date = date.today()
    
    total_days = (end_date - start_date).days
    return total_days / 365.25


def generate_otp(length: int = 6) -> str:
    """
    Generate OTP code
    """
    import random
    digits = "0123456789"
    return ''.join(random.choice(digits) for _ in range(length))


def mask_email(email: str) -> str:
    """
    Mask email address for privacy
    """
    if '@' not in email:
        return email
    
    local_part, domain = email.split('@')
    if len(local_part) <= 2:
        masked_local = local_part[0] + '*' * (len(local_part) - 1)
    else:
        masked_local = local_part[0] + '*' * (len(local_part) - 2) + local_part[-1]
    
    domain_parts = domain.split('.')
    if len(domain_parts) >= 2:
        masked_domain = '*' * len(domain_parts[0]) + '.' + '.'.join(domain_parts[1:])
    else:
        masked_domain = '*' * len(domain)
    
    return f"{masked_local}@{masked_domain}"


def mask_mobile(mobile: str) -> str:
    """
    Mask mobile number for privacy
    """
    if len(mobile) <= 4:
        return mobile
    
    visible_digits = 4
    masked = '*' * (len(mobile) - visible_digits) + mobile[-visible_digits:]
    return masked