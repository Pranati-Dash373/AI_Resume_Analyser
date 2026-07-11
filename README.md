# 🤖 AI Resume Analyser & Job Match Platform

A full-stack AI-powered web application that analyses resumes and matches them to job listings using Large Language Models.

## 🌟 Features

- 📄 **PDF Resume Upload** — Drag and drop your resume
- 🤖 **AI Analysis** — Get a score out of 100 with detailed feedback
- ✅ **Strengths Detection** — Know what you're doing right
- ⚠️ **Weakness Detection** — Know what needs improvement
- 🔍 **Missing Keywords** — See what keywords are missing
- 💡 **Suggestions** — Get actionable improvement tips
- 🎯 **Live Job Matching** — Real listings pulled from LinkedIn, Naukri, Glassdoor, Indeed and more (via JSearch), matched to your resume by role
- 📊 **Match Percentage** — See how well you fit each job
- ✨ **ATS-Friendly Resume Optimizer** — Rewrites your resume for a specific job, filling in missing keywords, in an ATS-parseable format (single column, standard headers, no graphics)

## 🛠️ Tech Stack

### Frontend
- React + Vite
- TailwindCSS
- Axios
- React Dropzone
- React Router DOM

### Backend
- Python
- FastAPI
- SQLAlchemy
- PyMuPDF (PDF text extraction)
- JWT Authentication

### Database
- SQLite

### AI
- Groq API (LLaMA 3.3 70B model)

### Job Data
- JSearch API (RapidAPI) — aggregates real-time postings from LinkedIn, Naukri, Glassdoor, Indeed, ZipRecruiter and more

## 📁 Project Structure

```
Resume_analyser/
├── backend/
│   ├── main.py                      # FastAPI app entry point
│   ├── database.py                  # Database connection
│   ├── models.py                    # Database models (User, Resume, ExternalJob)
│   ├── routers/
│   │   ├── auth.py                  # Login & register endpoints
│   │   ├── resume.py                # Resume upload endpoint
│   │   └── jobs.py                  # Live job search, matching & optimize endpoints
│   └── services/
│       ├── ai_service.py            # Groq AI integration
│       ├── pdf_service.py           # PDF text extraction
│       └── job_search_service.py    # JSearch (RapidAPI) live job listings
└── frontend/
    └── src/
        ├── App.jsx                  # Main router
        └── pages/
            ├── Upload.jsx           # Upload page
            ├── Dashboard.jsx        # Results + live job matches
            └── OptimizedResume.jsx  # ATS-optimized resume for a chosen job
```

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key (free at https://console.groq.com)
- RapidAPI Key for JSearch (free, no card required — sign up at https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch, subscribe to the free BASIC plan, copy the key shown under "X-RapidAPI-Key")

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the backend folder (see `.env.example`):
```
GROQ_API_KEY=your-groq-api-key
JWT_SECRET=your-secret-key
RAPIDAPI_KEY=your-rapidapi-key
```

Start the backend:
```bash
python -m uvicorn main:app
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Open in Browser
```

http://localhost:5173

```

## 🔄 How It Works
```
1. User up