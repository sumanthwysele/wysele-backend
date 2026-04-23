from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.contact import ContactInquiry
from app.schemas.contact import ContactCreate, ContactResponse
from app.schemas.pagination import PaginatedResponse, paginate

router = APIRouter()

# PUBLIC: Submit inquiry
@router.post("/", response_model=ContactResponse)
def submit_inquiry(contact_in: ContactCreate, db: Session = Depends(deps.get_db)):
    new_inquiry = ContactInquiry(**contact_in.model_dump())
    db.add(new_inquiry)
    db.commit()
    db.refresh(new_inquiry)
    return new_inquiry

# ADMIN ONLY: Get all inquiries (paginated)
@router.get("/all", response_model=PaginatedResponse[ContactResponse])
def get_all_inquiries(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=100, description="Results per page")
):
    query = db.query(ContactInquiry).order_by(ContactInquiry.created_at.desc())
    return paginate(query, page, limit)

# SUPER_ADMIN ONLY: Delete inquiry
@router.delete("/{inquiry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inquiry(
    inquiry_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_super_admin)
):
    inquiry = db.query(ContactInquiry).filter(ContactInquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    db.delete(inquiry)
    db.commit()
