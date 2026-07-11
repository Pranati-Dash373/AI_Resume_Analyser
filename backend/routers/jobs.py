import datetime
import traceback

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import ExternalJob, Resume
from services.ai_service import derive_job_search_query, match_resume_to_job, optimize_resume_for_job
from services.job_search_service import search_jobs, JobSearchError

router = APIRouter(prefix="/jobs", tags=["jobs"])

MAX_JOBS_TO_SCORE = 8
CACHE_MINUTES = 60  # avoid re-hitting the live job API on every dashboard reload


@router.get("/match/{resume_id}")
def match_jobs(
    resume_id: int,
    role: str | None = Query(None, description="Override the AI-inferred job title"),
    location: str = Query("India", description="Location to search near"),
    refresh: bool = Query(False, description="Force a fresh live search, bypassing the cache"),
    db: Session = Depends(get_db),
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(404, "Resume not found")

    cached = (
        db.query(ExternalJob)
        .filter(ExternalJob.resume_id == resume_id)
        .order_by(ExternalJob.fetched_at.desc())
        .all()
    )
    fresh_cutoff = datetime.datetime.utcnow() - datetime.timedelta(minutes=CACHE_MINUTES)
    use_cache = (
        not refresh
        and not role
        and cached
        and cached[0].fetched_at is not None
        and cached[0].fetched_at > fresh_cutoff
    )

    if use_cache:
        job_rows = cached[:MAX_JOBS_TO_SCORE]
        query_used = "cached results"
    else:
        try:
            search_query = role or derive_job_search_query(resume.raw_text).get("role", "Software Engineer")
            listings = search_jobs(query=search_query, location=location, num_results=MAX_JOBS_TO_SCORE)
        except JobSearchError as e:
            raise HTTPException(502, str(e))
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
            # last non-framework frame, so the error is self-diagnosing without needing the server console
            last_frame = [line for line in tb.strip().splitlines() if line.strip().startswith("File \"")][-1:]
            frame_info = last_frame[0].strip() if last_frame else ""
            raise HTTPException(
                500,
                f"Error preparing job search: {type(e).__name__}: {e} | {frame_info}"
            )

        # clear stale cached listings for this resume before storing fresh ones
        db.query(ExternalJob).filter(ExternalJob.resume_id == resume_id).delete()
        db.commit()

        job_rows = []
        for listing in listings:
            row = ExternalJob(
                resume_id=resume_id,
                external_id=listing["external_id"],
                title=listing["title"],
                company=listing["company"],
                location=listing["location"],
                description=listing["description"],
                apply_link=listing["apply_link"],
                source=listing["source"],
            )
            db.add(row)
            job_rows.append(row)
        db.commit()
        for row in job_rows:
            db.refresh(row)
        query_used = search_query

    if not job_rows:
        return {"matches": [], "query_used": query_used}

    matches = []
    for job in job_rows:
        job_dict = {"title": job.title, "company": job.company, "description": job.description, "skills": ""}
        try:
            match = match_resume_to_job(resume.raw_text, job_dict)
        except Exception:
            traceback.print_exc()
            continue
        matches.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "source": job.source,
            "apply_link": job.apply_link,
            **match,
        })
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return {"matches": matches, "query_used": query_used}


@router.get("/optimize/{resume_id}/{job_id}")
def optimize_resume(resume_id: int, job_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    job = db.query(ExternalJob).filter(ExternalJob.id == job_id, ExternalJob.resume_id == resume_id).first()
    if not resume:
        raise HTTPException(404, "Resume not found")
    if not job:
        raise HTTPException(404, "Job not found")

    job_dict = {"title": job.title, "company": job.company, "description": job.description, "skills": ""}
    try:
        result = optimize_resume_for_job(resume.raw_text, job_dict)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, f"Error optimizing resume: {str(e)}")

    return {
        "job_title": job.title,
        "company": job.company,
        "source": job.source,
        "apply_link": job.apply_link,
        "optimized_resume": result["optimized_resume"],
        "changes_made": result["changes_made"],
        "keywords_added": result["keywords_added"],
        "ats_score": result["ats_score"],
    }
