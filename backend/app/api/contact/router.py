"""
Contact API endpoints for Thathvamasi HR Consultancy
"""

from fastapi import APIRouter

router = APIRouter(prefix="/contact", tags=["contact"])


@router.get("/")
async def contact_info():
    """Get contact information"""
    return {"message": "Contact information endpoint - Under construction"}


@router.post("/enquiry")
async def submit_enquiry():
    """Submit contact enquiry"""
    return {"message": "Contact enquiry endpoint - Under construction"}


@router.get("/enquiries")
async def list_enquiries():
    """List all enquiries (admin only)"""
    return {"message": "Enquiries listing endpoint - Under construction"}


@router.get("/enquiries/{enquiry_id}")
async def get_enquiry(enquiry_id: str):
    """Get enquiry by ID (admin only)"""
    return {"message": f"Get enquiry {enquiry_id} - Under construction"}