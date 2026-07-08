from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Resume
from services.pdf_service import extract_text_from_pdf
from services.ai_service import analyse_resume
import json
import traceback

router = APIRouter(prefix="/resume", tags=["resume"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(400, "Only PDF files accepted")
        file_bytes = await file.read()
        raw_text = extract_text_from_pdf(file_bytes)
        if len(raw_text) < 50:
            raise HTTPException(400, "Could not extract text from PDF")
        analysis = analyse_resume(raw_text)
        resume = Resume(
            user_id=user_id,
            filename=file.filename,
            raw_text=raw_text,
            score=analysis["score"],
            feedback=json.dumps(analysis)
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return {"resume_id": resume.id, "analysis": analysis}
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, f"Error: {str(e)}")

@router.get("/{resume_id}")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(404, "Resume not found")
        return {
            "filename": resume.filename,
            "score": resume.score,
            "feedback": json.loads(resume.feedback)
        }
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, f"Error: {str(e)}")