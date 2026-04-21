from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, index=True) # Organisation, Innovation, etc.
    image_url = Column(String) # URL to the uploaded photo
    read_time = Column(String) # e.g., "10 MIN READ"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Author Info
    author_id = Column(Integer, ForeignKey("users.id"))
    author_name = Column(String) # For fast display without extra joins