from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Job, Resume
from services.ai_service import match_resume_to_job
import json

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/match/{resume_id}")
def match_jobs(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        return {"error": "Resume not found"}
    jobs = db.query(Job).all()
    matches = []
    for job in jobs:
        job_dict = {
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "skills": job.skills
        }
        match = match_resume_to_job(resume.raw_text, job_dict)
        matches.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            **match
        })
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return {"matches": matches}