from groq import Groq
import json
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=60.0
)

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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    text = response.choices[0].message.content.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


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
REQUIRED SKILLS: {job["skills"]}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    text = response.choices[0].message.content.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def optimize_resume_for_job(resume_text: str, job: dict) -> dict:
    prompt = f"""You are an expert resume writer.
Rewrite this resume to match the job description below.

STRICT RULES:
- Maximum 1 page resume — keep it SHORT and CONCISE
- Maximum 3-4 bullet points per section
- Each bullet point maximum 1 line
- Only include MOST RELEVANT experience for this job
- Remove irrelevant experience
- Use action verbs (Developed, Built, Managed, Led)
- Add missing keywords from job description naturally
- Keep education short — just degree, college, year
- Skills section — comma separated, one line only
- Do NOT make up fake experience
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
REQUIRED SKILLS: {job["skills"]}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    text = response.choices[0].message.content.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())