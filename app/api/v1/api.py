from fastapi import APIRouter, Depends
from app.api.v1.endpoints import auth, blogs, admins, contact, jobs
from app.api import deps

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])
api_router.include_router(admins.router, prefix="/admins", tags=["Admins"], dependencies=[Depends(deps.get_current_super_admin)])
api_router.include_router(contact.router, prefix="/contact", tags=["Contact"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])