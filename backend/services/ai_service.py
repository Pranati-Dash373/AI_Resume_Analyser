from groq import Groq
import json
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=60.0
)

MODEL = "llama-3.3-70b-versatile"


def _call_json(prompt: str, temperature: float = 0.3) -> dict:
    """Send a prompt expecting a single JSON object back, and parse it."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    text = response.choices[0].message.content.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def analyse_resume(resume_text: str) -> dict:
    prompt = f"""You are an expert resume reviewer.
Analyse this resume and respond with ONLY valid JSON, no markdown, no extra text:

{{
  "score": 75,
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "missing_keywords": ["keyword 1", "keyword 2"],
  "suggestions": ["suggestion 1", "suggestion 2"],
  "summary": "2 sentence summary here"
}}

RESUME:
{resume_text}"""
    return _call_json(prompt)


def derive_job_search_query(resume_text: str) -> dict:
    """
    Infer the best job title/role and top keywords to search live job
    boards with, based on the resume content.
    """
    prompt = f"""You are a technical recruiter. Based on this resume, suggest the SINGLE
best job title to search for on job boards (e.g. "Software Engineer",
"Backend Developer", "Data Analyst") and up to 5 top technical keywords.
Respond ONLY with valid JSON, no markdown, no extra text:

{{
  "role": "Software Engineer",
  "keywords": ["Python", "FastAPI", "SQL"]
}}

RESUME:
{resume_text}"""
    return _call_json(prompt)


def match_resume_to_job(resume_text: str, job: dict) -> dict:
    prompt = f"""You are a technical recruiter. Score how well this resume matches the job.
Respond ONLY with valid JSON, no markdown, no extra text:

{{
  "match_score": 75,
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "recommendation": "one sentence here"
}}

RESUME:
{resume_text}

JOB TITLE: {job["title"]}
JOB DESCRIPTION: {job["description"]}
REQUIRED SKILLS: {job.get("skills", "")}"""
    return _call_json(prompt)


def optimize_resume_for_job(resume_text: str, job: dict) -> dict:
    prompt = f"""You are an expert resume writer specializing in ATS (Applicant Tracking
System) optimization.
Rewrite this resume to match the job description below.

STRICT CONTENT RULES:
- Maximum 1 page resume — keep it SHORT and CONCISE
- Maximum 3-4 bullet points per section
- Each bullet point maximum 1 line
- Only include MOST RELEVANT experience for this job
- Remove irrelevant experience
- Use action verbs (Developed, Built, Managed, Led)
- Add missing keywords from the job description naturally, wherever they are
  truthfully applicable — do not keyword-stuff
- Keep education short — just degree, college, year
- Skills section — comma separated, one line only
- Do NOT make up fake experience

STRICT ATS-FRIENDLY FORMATTING RULES:
- Use ONLY standard section headers in ALL CAPS on their own line: SUMMARY,
  SKILLS, EXPERIENCE, EDUCATION, PROJECTS, CERTIFICATIONS (only include
  sections that have content)
- Single column, top-to-bottom, reverse-chronological order — no tables,
  no multi-column layouts, no text boxes
- No emojis, no special/decorative unicode characters, no icons
- Use a plain hyphen "-" for bullet points, never "•" or other symbols
- Use standard date format: "Mon YYYY - Mon YYYY" or "Mon YYYY - Present"
- No headers/footers, no images, no graphics
- First line = full name. Second line = contact info (email, phone, location)
  on one line, comma separated
- Return ONLY valid JSON, no markdown, no extra text

Return this exact JSON:
{{
  "optimized_resume": "full rewritten resume text here — maximum 1 page worth of content",
  "changes_made": ["change 1", "change 2", "change 3"],
  "keywords_added": ["keyword1", "keyword2"],
  "ats_score": <number 0-100>
}}

ORIGINAL RESUME:
{resume_text}

JOB TITLE: {job["title"]}
JOB COMPANY: {job["company"]}
JOB DESCRIPTION: {job["description"]}
REQUIRED SKILLS: {job.get("skills", "")}"""
    return _call_json(prompt)
