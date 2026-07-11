from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id        = Column(Integer, primary_key=True, index=True)
    email     = Column(String, unique=True, index=True)
    hashed_pw = Column(String)
    name      = Column(String)
    resumes   = relationship("Resume", back_populates="owner")

class Resume(Base):
    __tablename__ = "resumes"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"))
    filename   = Column(String)
    raw_text   = Column(Text)
    score      = Column(Float)
    feedback   = Column(Text)   # JSON string from Claude
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner      = relationship("User", back_populates="resumes")

class ExternalJob(Base):
    """
    A live job listing fetched from the JSearch API for a specific resume.
    Cached per-resume so /jobs/optimize can look the listing back up
    without re-hitting the external API (RapidAPI free tier is
    rate-limited to 200 requests/month).
    """
    __tablename__ = "external_jobs"
    id          = Column(Integer, primary_key=True, index=True)
    resume_id   = Column(Integer, ForeignKey("resumes.id"))
    external_id = Column(String)          # job_id from JSearch, not unique across resumes
    title       = Column(String)
    company     = Column(String)
    location    = Column(String)
    description = Column(Text)
    apply_link  = Column(String)
    source      = Column(String)          # e.g. "LinkedIn", "Naukri.com", "Glassdoor", "Indeed"
    fetched_at  = Column(DateTime, default=datetime.datetime.utcnow)