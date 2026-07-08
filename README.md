# 🤖 AI Resume Analyser & Job Match Platform

A full-stack AI-powered web application that analyses resumes and matches them to job listings using Large Language Models.

## 🌟 Features

- 📄 **PDF Resume Upload** — Drag and drop your resume
- 🤖 **AI Analysis** — Get a score out of 100 with detailed feedback
- ✅ **Strengths Detection** — Know what you're doing right
- ⚠️ **Weakness Detection** — Know what needs improvement
- 🔍 **Missing Keywords** — See what keywords are missing
- 💡 **Suggestions** — Get actionable improvement tips
- 🎯 **Job Matching** — Match your resume against job listings
- 📊 **Match Percentage** — See how well you fit each job

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

## 📁 Project Structure

Resume_analyser/ ├── backend/ │ ├── main.py # FastAPI app entry point │ ├── database.py # Database connection │ ├── models.py # Database models │ ├── seed_jobs.py # Sample job data │ ├── routers/ │ │ ├── auth.py # Login & register endpoints │ │ ├── resume.py # Resume upload endpoint │ │ └── jobs.py # Job matching endpoint │ └── services/ │ ├── ai_service.py # Groq AI integration │ └── pdf_service.py # PDF text extraction └── frontend/ └── src/ ├── App.jsx # Main router └── pages/ ├── Upload.jsx # Upload page └── Dashboard.jsx # Results page

```

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key (free at https://console.groq.com)

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pymupdf groq python-multipart python-dotenv passlib bcrypt python-jose
```

Create `.env` file in backend folder:
```

GROQ_API_KEY=your-groq-api-key JWT_SECRET=your-secret-key

```

Seed the database:
```bash
python seed_jobs.py
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

1. User uploads PDF resume
2. PyMuPDF extracts text from PDF
3. Text sent to Groq AI (LLaMA model)
4. AI returns score, strengths, weaknesses, suggestions
5. Resume matched against jobs in database
6. AI calculates match percentage for each job
7. Results displayed on dashboard

```

## 📸 Screenshots

### Upload Page
- Clean drag and drop interface
- Supports PDF files only

### Dashboard
- Resume score out of 100
- Color coded progress bar
- Missing keywords highlighted
- Strengths and suggestions
- Job matches ranked by compatibility

## 🔮 Future Improvements

- [ ] User authentication and history
- [ ] Cover letter generator
- [ ] Real job listings from LinkedIn API
- [ ] Email notifications for job matches
- [ ] Resume builder
- [ ] Deploy on cloud

## 👩‍💻 Built By

**Pranati Dash**  
Computer Science Graduate  
Passionate about AI and Full Stack Development

## 📄 License

MIT License — feel free to use and modify!