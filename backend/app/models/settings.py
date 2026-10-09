"""
Settings and configuration models
"""

from typing import Optional, Dict, List
from pydantic import Field, EmailStr
from app.models.base import BaseDBModel
from app.utils.helpers import validate_indian_mobile


class ContactSettings(BaseDBModel):
    """
    Contact information settings
    """
    company_name: str = Field(..., description="Company name")
    office_address: str = Field(..., description="Office address")
    email: EmailStr = Field(..., description="Primary email address")
    phone: str = Field(..., description="Primary phone number")
    whatsapp: Optional[str] = Field(None, description="WhatsApp number")
    alternate_phone: Optional[str] = Field(None, description="Alternate phone number")
    fax: Optional[str] = Field(None, description="Fax number")
    
    # Social media
    facebook: Optional[str] = Field(None, description="Facebook URL")
    twitter: Optional[str] = Field(None, description="Twitter URL")
    linkedin: Optional[str] = Field(None, description="LinkedIn URL")
    instagram: Optional[str] = Field(None, description="Instagram URL")
    youtube: Optional[str] = Field(None, description="YouTube URL")
    
    # Business hours
    business_hours: Optional[str] = Field(None, description="Business hours")
    timezone: str = Field(default="Asia/Kolkata", description="Timezone")
    
    # Google Maps
    google_maps_embed: Optional[str] = Field(None, description="Google Maps embed code")
    latitude: Optional[float] = Field(None, description="Map latitude")
    longitude: Optional[float] = Field(None, description="Map longitude")
    
    @validator('phone', 'whatsapp', 'alternate_phone')
    def validate_phone_numbers(cls, v):
        if v and not validate_indian_mobile(v):
            raise ValueError('Invalid Indian mobile number format')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "company_name": "Thathvamasi HR Consultancy",
                "office_address": "123 Main Street, Coimbatore, Tamil Nadu 641001",
                "email": "contact@thathvamasi.com",
                "phone": "9876543210",
                "whatsapp": "9876543210",
                "facebook": "https://facebook.com/thathvamasi",
                "linkedin": "https://linkedin.com/company/thathvamasi",
                "business_hours": "Mon-Fri: 9:00 AM - 6:00 PM, Sat: 9:00 AM - 1:00 PM",
                "timezone": "Asia/Kolkata"
            }
        }


class SEOSettings(BaseDBModel):
    """
    SEO settings
    """
    site_title: str = Field(..., description="Website title")
    site_description: str = Field(..., description="Website description")
    site_keywords: List[str] = Field(default_factory=list, description="Website keywords")
    site_author: Optional[str] = Field(None, description="Site author")
    site_language: str = Field(default="en", description="Site language")
    
    # Social sharing
    og_image: Optional[str] = Field(None, description="Default Open Graph image")
    og_type: str = Field(default="website", description="Open Graph type")
    twitter_site: Optional[str] = Field(None, description="Twitter site handle")
    twitter_creator: Optional[str] = Field(None, description="Twitter creator handle")
    
    # Verification
    google_site_verification: Optional[str] = Field(None, description="Google Site Verification code")
    bing_site_verification: Optional[str] = Field(None, description="Bing Site Verification code")
    
    # Analytics
    google_analytics_id: Optional[str] = Field(None, description="Google Analytics ID")
    google_tag_manager_id: Optional[str] = Field(None, description="Google Tag Manager ID")
    
    # Structured data
    structured_data: Optional[Dict] = Field(default_factory=dict, description="Structured data/JSON-LD")
    
    class Config:
        schema_extra = {
            "example": {
                "site_title": "Thathvamasi HR Consultancy",
                "site_description": "Professional HR and Recruitment Services in Coimbatore",
                "site_keywords": ["HR", "Recruitment", "Staffing", "Coimbatore", "HR Consultancy"],
                "site_language": "en",
                "google_analytics_id": "G-XXXXXXXXXX"
            }
        }


class EmailSettings(BaseDBModel):
    """
    Email configuration settings
    """
    smtp_host: str = Field(..., description="SMTP host")
    smtp_port: int = Field(default=587, description="SMTP port")
    smtp_username: str = Field(..., description="SMTP username")
    smtp_password: str = Field(..., description="SMTP password")
    use_tls: bool = Field(default=True, description="Use TLS")
    use_ssl: bool = Field(default=False, description="Use SSL")
    
    # Email addresses
    from_email: EmailStr = Field(..., description="Default from email")
    admin_email: EmailStr = Field(..., description="Admin notification email")
    support_email: Optional[EmailStr] = Field(None, description="Support email")
    noreply_email: Optional[EmailStr] = Field(None, description="No-reply email")
    
    # Templates
    email_templates: Optional[Dict] = Field(default_factory=dict, description="Email templates configuration")
    
    class Config:
        schema_extra = {
            "example": {
                "smtp_host": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_username": "contact@thathvamasi.com",
                "smtp_password": "********",
                "use_tls": True,
                "from_email": "noreply@thathvamasi.com",
                "admin_email": "admin@thathvamasi.com"
            }
        }


class FileUploadSettings(BaseDBModel):
    """
    File upload settings
    """
    # Resume upload
    max_resume_size_mb: int = Field(default=5, description="Maximum resume size in MB")
    allowed_resume_types: List[str] = Field(
        default=["pdf", "doc", "docx"],
        description="Allowed resume file types"
    )
    
    # Job description upload
    max_jd_size_mb: int = Field(default=10, description="Maximum JD size in MB")
    allowed_jd_types: List[str] = Field(
        default=["pdf", "doc", "docx"],
        description="Allowed JD file types"
    )
    
    # Image upload
    max_image_size_mb: int = Field(default=5, description="Maximum image size in MB")
    allowed_image_types: List[str] = Field(
        default=["jpg", "jpeg", "png", "gif", "webp"],
        description="Allowed image file types"
    )
    
    # Storage
    storage_provider: str = Field(default="cloudinary", description="Storage provider")
    cloudinary_folder: str = Field(default="thathvamasi", description="Cloudinary folder")
    local_storage_path: Optional[str] = Field(None, description="Local storage path")
    
    # Security
    scan_for_viruses: bool = Field(default=True, description="Scan files for viruses")
    rename_uploaded_files: bool = Field(default=True, description="Rename uploaded files")
    
    class Config:
        schema_extra = {
            "example": {
                "max_resume_size_mb": 5,
                "allowed_resume_types": ["pdf", "doc", "docx"],
                "max_jd_size_mb": 10,
                "max_image_size_mb": 5,
                "storage_provider": "cloudinary",
                "cloudinary_folder": "thathvamasi",
                "scan_for_viruses": True
            }
        }


class SecuritySettings(BaseDBModel):
    """
    Security settings
    """
    # Rate limiting
    rate_limit_per_minute: int = Field(default=100, description="Requests per minute per IP")
    rate_limit_per_hour: int = Field(default=1000, description="Requests per hour per IP")
    
    # Authentication
    jwt_secret_key: str = Field(..., description="JWT secret key")
    jwt_access_token_expire_minutes: int = Field(default=60*24*7, description="Access token expiry in minutes")
    jwt_refresh_token_expire_days: int = Field(default=30, description="Refresh token expiry in days")
    
    # Password policy
    password_min_length: int = Field(default=8, description="Minimum password length")
    require_uppercase: bool = Field(default=True, description="Require uppercase letters")
    require_lowercase: bool = Field(default=True, description="Require lowercase letters")
    require_numbers: bool = Field(default=True, description="Require numbers")
    require_special_chars: bool = Field(default=True, description="Require special characters")
    
    # Session
    session_timeout_minutes: int = Field(default=30, description="Session timeout in minutes")
    max_login_attempts: int = Field(default=5, description="Maximum login attempts before lockout")
    lockout_duration_minutes: int = Field(default=15, description="Account lockout duration in minutes")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "https://thathvamasi.com"],
        description="Allowed CORS origins"
    )
    
    # reCAPTCHA
    recaptcha_site_key: Optional[str] = Field(None, description="reCAPTCHA site key")
    recaptcha_secret_key: Optional[str] = Field(None, description="reCAPTCHA secret key")
    enable_recaptcha: bool = Field(default=False, description="Enable reCAPTCHA protection")
    
    class Config:
        schema_extra = {
            "example": {
                "rate_limit_per_minute": 100,
                "jwt_access_token_expire_minutes": 10080,
                "password_min_length": 8,
                "cors_origins": ["http://localhost:3000", "https://thathvamasi.com"],
                "enable_recaptcha": True
            }
        }


class NotificationSettings(BaseDBModel):
    """
    Notification settings
    """
    # Email notifications
    notify_admin_on_candidate: bool = Field(default=True, description="Notify admin on new candidate")
    notify_admin_on_client: bool = Field(default=True, description="Notify admin on new client")
    notify_admin_on_contact: bool = Field(default=True, description="Notify admin on new contact")
    
    # Candidate notifications
    notify_candidate_on_submission: bool = Field(default=True, description="Notify candidate on submission")
    notify_candidate_on_status_change: bool = Field(default=True, description="Notify candidate on status change")
    
    # Client notifications
    notify_client_on_submission: bool = Field(default=True, description="Notify client on submission")
    notify_client_on_status_change: bool = Field(default=True, description="Notify client on status change")
    
    # WhatsApp notifications
    enable_whatsapp_notifications: bool = Field(default=False, description="Enable WhatsApp notifications")
    whatsapp_business_id: Optional[str] = Field(None, description="WhatsApp Business ID")
    whatsapp_access_token: Optional[str] = Field(None, description="WhatsApp Access Token")
    
    # SMS notifications
    enable_sms_notifications: bool = Field(default=False, description="Enable SMS notifications")
    sms_provider: Optional[str] = Field(None, description="SMS provider")
    sms_api_key: Optional[str] = Field(None, description="SMS API key")
    
    class Config:
        schema_extra = {
            "example": {
                "notify_admin_on_candidate": True,
                "notify_candidate_on_submission": True,
                "notify_client_on_submission": True,
                "enable_whatsapp_notifications": False
            }
        }


class WebsiteSettings(BaseDBModel):
    """
    General website settings
    """
    # General
    site_name: str = Field(..., description="Website name")
    site_tagline: Optional[str] = Field(None, description="Website tagline")
    site_logo: Optional[str] = Field(None, description="Website logo URL")
    favicon: Optional[str] = Field(None, description="Favicon URL")
    
    # Theme
    primary_color: str = Field(default="#3b82f6", description="Primary color")
    secondary_color: str = Field(default="#10b981", description="Secondary color")
    font_family: str = Field(default="Inter", description="Font family")
    
    # Features
    enable_blog: bool = Field(default=True, description="Enable blog feature")
    enable_candidate_portal: bool = Field(default=True, description="Enable candidate portal")
    enable_client_portal: bool = Field(default=True, description="Enable client portal")
    enable_whatsapp_chat: bool = Field(default=True, description="Enable WhatsApp chat")
    enable_live_chat: bool = Field(default=False, description="Enable live chat")
    
    # Maintenance
    maintenance_mode: bool = Field(default=False, description="Maintenance mode")
    maintenance_message: Optional[str] = Field(None, description="Maintenance message")
    
    # Cache
    enable_cache: bool = Field(default=True, description="Enable caching")
    cache_duration_minutes: int = Field(default=60, description="Cache duration in minutes")
    
    class Config:
        schema_extra = {
            "example": {
                "site_name": "Thathvamasi HR Consultancy",
                "site_tagline": "Connecting Talent with Opportunity",
                "primary_color": "#3b82f6",
                "secondary_color": "#10b981",
                "enable_blog": True,
                "enable_whatsapp_chat": True,
                "maintenance_mode": False
            }
        }


class Settings(BaseDBModel):
    """
    Complete settings model
    """
    contact: ContactSettings
    seo: SEOSettings
    email: EmailSettings
    file_upload: FileUploadSettings
    security: SecuritySettings
    notifications: NotificationSettings
    website: WebsiteSettings
    
    # Version and metadata
    version: str = Field(default="1.0.0", description="Settings version")
    last_updated: Optional[str] = Field(None, description="Last updated timestamp")
    updated_by: Optional[str] = Field(None, description="Updated by user")
    
    class Config:
        schema_extra = {
            "example": {
                "contact": {
                    "company_name": "Thathvamasi HR Consultancy",
                    "office_address": "Coimbatore, Tamil Nadu",
                    "email": "contact@thathvamasi.com",
                    "phone": "9876543210"
                },
                "seo": {
                    "site_title": "Thathvamasi HR Consultancy",
                    "site_description": "Professional HR Services"
                },
                "email": {
                    "smtp_host": "smtp.gmail.com",
                    "from_email": "noreply@thathvamasi.com"
                },
                "website": {
                    "site_name": "Thathvamasi HR",
                    "enable_blog": True
                }
            }
        }


class SettingsUpdate(BaseDBModel):
    """
    Model for updating settings
    """
    contact: Optional[ContactSettings] = None
    seo: Optional[SEOSettings] = None
    email: Optional[EmailSettings] = None
    file_upload: Optional[FileUploadSettings] = None
    security: Optional[SecuritySettings] = None
    notifications: Optional[NotificationSettings] = None
    website: Optional[WebsiteSettings] = None


class SettingsResponse(BaseDBModel):
    """
    Settings response model for API
    """
    settings: Settings
    success: bool = True
    message: Optional[str] = None