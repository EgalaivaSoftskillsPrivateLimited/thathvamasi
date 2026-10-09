"""
Contact API endpoints for Thathvamasi HR Consultancy
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.models.contact_model import ContactEnquiry
from app.core.config import settings

router = APIRouter(tags=["contact"])


class EnquiryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    mobile: Optional[str] = Field(None, max_length=50)
    subject: Optional[str] = Field("General Enquiry", max_length=255)
    message: str = Field(..., min_length=5)


class EnquiryResponse(BaseModel):
    id: UUID
    name: str
    email: str
    mobile: Optional[str]
    subject: str
    message: str
    status: str
    created_at: str

    class Config:
        from_attributes = True


@router.get("/")
async def contact_info():
    """Get corporate contact details"""
    return {
        "company": "Thathvamasi HR Consultancy",
        "headquarters": "Avinashi Road, Peelamedu, Coimbatore - 641004, Tamil Nadu, India",
        "phone": "+91 94422 18900",
        "email": "info@thathvamasi.com",
        "working_hours": "Monday - Saturday: 9:00 AM - 6:30 PM IST"
    }


@router.post("/enquiry")
async def submit_enquiry(
    enquiry: EnquiryCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a general or recruitment enquiry from the website contact form
    """
    try:
        new_enquiry = ContactEnquiry(
            name=enquiry.name.strip(),
            email=enquiry.email.strip().lower(),
            mobile=enquiry.mobile.strip() if enquiry.mobile else None,
            subject=enquiry.subject.strip() if enquiry.subject else "General Recruitment Query",
            message=enquiry.message.strip(),
            status="new"
        )
        db.add(new_enquiry)
        await db.commit()
        await db.refresh(new_enquiry)

        return {
            "success": True,
            "message": "Enquiry registered successfully. Our Coimbatore advisory desk will connect with you shortly.",
            "data": {
                "id": str(new_enquiry.id),
                "name": new_enquiry.name,
                "email": new_enquiry.email,
                "subject": new_enquiry.subject,
                "status": new_enquiry.status,
                "created_at": new_enquiry.created_at.isoformat()
            }
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit enquiry: {str(e)}"
        )


@router.get("/enquiries")
async def list_enquiries(
    db: AsyncSession = Depends(get_db)
):
    """
    List all enquiries for the HR Command Center
    """
    try:
        stmt = select(ContactEnquiry).order_by(desc(ContactEnquiry.created_at)).limit(100)
        result = await db.execute(stmt)
        enquiries = result.scalars().all()

        data = []
        for e in enquiries:
            data.append({
                "id": str(e.id),
                "name": e.name,
                "email": e.email,
                "mobile": e.mobile or "Not Provided",
                "subject": e.subject,
                "message": e.message,
                "status": e.status,
                "date": e.created_at.strftime("%b %d, %Y") if e.created_at else ""
            })

        return {
            "success": True,
            "count": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve enquiries: {str(e)}"
        )