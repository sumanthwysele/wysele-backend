from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base_class import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    applicant_name = Column(String, nullable=False)
    applicant_email = Column(String, nullable=False, index=True)
    applicant_phone = Column(String, nullable=False)
    resume_url = Column(String, nullable=False)
    notice_period = Column(String, nullable=False)
    applied_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    job = relationship("Job", back_populates="applications")

    # One applicant can apply only once per job
    __table_args__ = (
        UniqueConstraint("job_id", "applicant_email", name="uq_job_applicant"),
    )
