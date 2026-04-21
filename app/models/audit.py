from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.db.base_class import Base

class Audit(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)