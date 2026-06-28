from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utcnow)

    resumes = relationship("Resume", back_populates="owner", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    builder_draft = relationship(
        "BuilderDraft", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    raw_text_excerpt = Column(Text, default="")
    ats_score = Column(Integer, default=0)
    formatting_score = Column(Integer, default=0)
    keywords_score = Column(Integer, default=0)
    experience_score = Column(Integer, default=0)
    education_score = Column(Integer, default=0)
    found_keywords = Column(Text, default="")  # comma-separated
    missing_keywords = Column(Text, default="")  # comma-separated
    suggestions = Column(Text, default="")  # newline-separated
    created_at = Column(DateTime, default=utcnow)

    owner = relationship("User", back_populates="resumes")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, default="general")


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, default="Remote")
    job_type = Column(String, default="Full-time")  # Remote/On-Site/Hybrid
    employment_type = Column(String, default="Full-Time")  # Full-Time/Contract
    salary_min = Column(Integer, default=0)
    salary_max = Column(Integer, default=0)
    tags = Column(String, default="")  # comma-separated
    description = Column(Text, default="")
    posted_days_ago = Column(Integer, default=1)
    created_at = Column(DateTime, default=utcnow)

    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    status = Column(String, default="saved")  # saved, applied, interview, rejected
    created_at = Column(DateTime, default=utcnow)

    user = relationship("User", back_populates="applications")
    job = relationship("JobPosting", back_populates="applications")


class BuilderDraft(Base):
    __tablename__ = "builder_drafts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    content_json = Column(Text, default="{}")
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    user = relationship("User", back_populates="builder_draft")
