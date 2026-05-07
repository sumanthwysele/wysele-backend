from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class ApplicationCreate(BaseModel):
    name: str
    email: EmailStr
    phoneNo: str
    resume: str
    noticePeriod: str


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    applicant_name: str
    applicant_email: str
    applicant_phone: str
    resume_url: str
    notice_period: str
    applied_at: datetime
