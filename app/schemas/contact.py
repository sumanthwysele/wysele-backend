from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class ContactCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    location: Optional[str] = None
    message: str

class ContactResponse(ContactCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
