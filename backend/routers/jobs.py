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
            # last non-framework frame, so the 