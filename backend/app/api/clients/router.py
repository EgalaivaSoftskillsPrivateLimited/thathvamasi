"""
Clients & Employer Requisitions API endpoints for Thathvamasi HR Consultancy
"""

from typing import Optional, List
from uuid import UUID
import uuid
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.client_model import Client, HiringRequirement

router = APIRouter(tags=["clients"])


class ClientRequisitionCreate(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=255)
    contact_person: str = Field(..., min_length=2, max_length=255)
    designation: Optional[str] = Field("HR Director / Hiring Lead", max_length=100)
    email: EmailStr
    mobile: Optional[str] = Field("Not Provided", max_length=50)
    location: Optional[str] = Field("Coimbatore", max_length=255)
    industry: Optional[str] = Field("Corporate Enterprise", max_length=255)
    position: str = Field(..., min_length=2, max_length=255)
    vacancies: int = Field(1, ge=1)
    experience: Optional[str] = Field("3 - 6 Years", max_length=100)
    salary_range: Optional[str] = Field("Best in Industry", max_length=100)
    employment_type: Optional[str] = Field("permanent", max_length=50)
    timeline: Optional[str] = Field("Within 30 Days", max_length=100)
    jd_summary: Optional[str] = Field(None)

    # Support camelCase from frontend
    model_config = ConfigDict(
        populate_by_name=True
    )


@router.get("/")
async def list_clients(
    db: AsyncSession = Depends(get_db)
):
    """
    List all corporate clients and hiring requisitions for HR Command Center
    """
    try:
        stmt = select(Client).options(selectinload(Client.hiring_requirements)).order_by(desc(Client.created_at))
        result = await db.execute(stmt)
        clients = result.scalars().all()

        output = []
        for c in clients:
            reqs = c.hiring_requirements or []
            first_req = reqs[0] if reqs else None
            output.append({
                "id": str(c.id),
                "companyName": c.company_name,
                "contactPerson": c.contact_person_name,
                "email": c.company_email,
                "mobile": c.company_phone or "Not Provided",
                "designation": c.contact_person_designation or "Lead",
                "location": c.city or "Coimbatore",
                "industry": c.industry or "Corporate",
                "status": c.status,
                "submittedDate": c.created_at.strftime("%Y-%m-%d") if c.created_at else "",
                "position": first_req.position_title if first_req else "General Requirement",
                "vacancies": first_req.number_of_vacancies if first_req else 1,
                "experience": first_req.required_experience if first_req else "3-5 Yrs",
                "salaryRange": f"{first_req.salary_range_min or ''} - {first_req.salary_range_max or ''} INR" if first_req and first_req.salary_range_min else "Competitive",
                "hiringTimeline": first_req.expected_joining_timeline if first_req else "Immediate",
                "requirementsCount": len(reqs)
            })

        return {
            "success": True,
            "count": len(output),
            "data": output
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch clients: {str(e)}"
        )


@router.post("/requisition")
@router.post("/")
async def submit_requisition(
    data: ClientRequisitionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit client hiring requisition from the employer form
    """
    try:
        # Check if client exists by email or create new
        stmt = select(Client).where(Client.company_email == data.email.lower().strip())
        res = await db.execute(stmt)
        client = res.scalar_one_or_none()

        if not client:
            client = Client(
                company_name=data.company_name.strip(),
                company_email=data.email.lower().strip(),
                company_phone=data.mobile.strip() if data.mobile else None,
                contact_person_name=data.contact_person.strip(),
                contact_person_email=data.email.lower().strip(),
                contact_person_phone=data.mobile.strip() if data.mobile else "Not Provided",
                contact_person_designation=data.designation.strip() if data.designation else "HR Director",
                industry=data.industry.strip() if data.industry else "Corporate Enterprise",
                city=data.location.strip() if data.location else "Coimbatore",
                status="new",
                client_type="regular"
            )
            db.add(client)
            await db.flush()

        # Create hiring requirement
        req = HiringRequirement(
            client_id=client.id,
            position_title=data.position.strip(),
            number_of_vacancies=data.vacancies,
            job_location=data.location.strip() if data.location else "Coimbatore",
            required_experience=data.experience.strip() if data.experience else "3 - 6 Years",
            employment_type=data.employment_type.strip().lower() if data.employment_type else "permanent",
            expected_joining_timeline=data.timeline.strip() if data.timeline else "Within 30 Days",
            job_description=data.jd_summary.strip() if data.jd_summary else "Detailed specifications to be discussed during intake consultation.",
            status="open"
        )
        db.add(req)
        await db.commit()
        await db.refresh(client)
        await db.refresh(req)

        generated_ref = f"THC-REQ-{str(req.id)[:8].upper()}"

        return {
            "success": True,
            "message": "Client requisition registered successfully. Dedicated account manager assigned.",
            "data": {
                "id": generated_ref,
                "clientId": str(client.id),
                "requirementId": str(req.id),
                "companyName": client.company_name,
                "position": req.position_title,
                "vacancies": req.number_of_vacancies,
                "status": req.status,
                "date": client.created_at.strftime("%Y-%m-%d") if client.created_at else ""
            }
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit hiring requisition: {str(e)}"
        )


@router.patch("/{client_id}/status")
async def update_client_status(
    client_id: str,
    status_update: dict,
    db: AsyncSession = Depends(get_db)
):
    """Update status of a client or requisition"""
    try:
        new_status = status_update.get("status", "contacted")
        try:
            client_uuid = uuid.UUID(client_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid client ID format")

        stmt = select(Client).where(Client.id == client_uuid)
        res = await db.execute(stmt)
        client = res.scalar_one_or_none()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        client.status = new_status
        await db.commit()
        return {"success": True, "message": f"Status updated to {new_status}"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))