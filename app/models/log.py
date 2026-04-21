from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.base_class import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)  # e.g., "INFO" or "ERROR"
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)