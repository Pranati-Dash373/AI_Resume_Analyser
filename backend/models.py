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

class Job(Base):
    __tablename__ = "jobs"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String)
    company     = Column(String)
    description = Column(Text)
    skills      = Column(Text)   # comma-separated
    location    = Column(String)