from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core import security

router = APIRouter()

# --- 1. GET ALL ---
@router.get("/", response_model=List[UserResponse])
def read_admins(
    db: Session = Depends(deps.get_db)
):
    """
    Returns the list of all admins with their permission statuses.
    """
    return db.query(User).filter(User.role == "ADMIN").order_by(User.created_at.desc()).all()

# --- 2. PUT / EDIT DETAILS ---
@router.put("/{admin_id}", response_model=UserResponse)
def update_admin(
    admin_id: int,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db)
):
    """
    Update admin Identity, Security, or Control flags.
    """
    admin = db.query(User).filter(User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    update_data = user_in.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        password = update_data.pop("password")
        admin.hashed_password = security.get_password_hash(password)

    for field, value in update_data.items():
        setattr(admin, field, value)

    db.commit()
    db.refresh(admin)
    return admin

# --- 4. PATCH / PERMISSIONS ---
@router.patch("/{admin_id}/permissions", response_model=UserResponse)
def update_admin_permissions(
    admin_id: int,
    can_post: Optional[bool] = None,
    can_edit: Optional[bool] = None,
    db: Session = Depends(deps.get_db)
):
    """
    Specific endpoint to toggle an admin's ability to post or edit blogs.
    """
    admin = db.query(User).filter(User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    if can_post is not None:
        admin.can_post_blog = can_post
    if can_edit is not None:
        admin.can_edit_blog = can_edit
        
    db.commit()
    db.refresh(admin)
    return admin

# --- 5. PATCH / STATUS ---
@router.patch("/{admin_id}/status", response_model=UserResponse)
def toggle_admin_status(
    admin_id: int,
    active_status: bool,
    db: Session = Depends(deps.get_db)
):
    admin = db.query(User).filter(User.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    admin.is_active = active_status
    db.commit()
    db.refresh(admin)
    return admin