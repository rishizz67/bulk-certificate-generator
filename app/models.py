# SQLAlchemy database models
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    event_name = Column(String(200), nullable=False)
    organization = Column(String(200), nullable=False)

    status = Column(String(50), default="queued", nullable=False)

    total = Column(Integer, default=0)
    successful = Column(Integer, default=0)
    failed = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    certificates = relationship(
        "Certificate",
        back_populates="job",
        cascade="all, delete-orphan"
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    recipient_name = Column(String(200), nullable=False)
    recipient_email = Column(String(200), nullable=False)
    course = Column(String(200), nullable=False)

    status = Column(String(50), default="pending", nullable=False)

    file_path = Column(String(500), nullable=True)

    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship(
        "Job",
        back_populates="certificates"
    )