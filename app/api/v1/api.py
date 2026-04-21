from fastapi import APIRouter, Depends
from app.api.v1.endpoints import auth, blogs, admins, contact
from app.api import deps

api_router = APIRouter()

# 1. AUTH: Public for Login, Restricted for Registration (handled inside auth.py)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# 2. BLOGS: Public for GET, Admin-restricted for POST/PUT/DELETE (handled inside blogs.py)
api_router.include_router(blogs.router, prefix="/blogs", tags=["blogs"])

# 3. ADMIN MANAGEMENT: Strictly ROOT ONLY
# We apply the dependency here so it covers EVERY route in the admins file.
api_router.include_router(
    admins.router, 
    prefix="/admins", 
    tags=["admins"],
    dependencies=[Depends(deps.get_current_super_admin)]
)

api_router.include_router(contact.router, prefix="/contact", tags=["contact"])