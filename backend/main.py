from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth, resume, jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume Analyser API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(jobs.router)

@app.get("/")
def root():
    return {"message": "Resume Analyser API running"}