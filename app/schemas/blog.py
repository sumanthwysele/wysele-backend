from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Common properties
class BlogBase(BaseModel):
    title: str
    content: str
    category: str
    image_url: Optional[str] = None
    read_time: Optional[str] = "5 MIN READ"

# Properties to receive on blog creation
class BlogCreate(BlogBase):
    pass

# Properties to receive on blog update
class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    read_time: Optional[str] = None

# Properties to return to the client
class BlogResponse(BlogBase):
    id: int
    author_id: int
    author_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True