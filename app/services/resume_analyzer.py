from app.services.resume_context import get_full_resume
from app.services.llm_service import get_llm_smart

llm = get_llm_smart()

def analyze_resume():

    context = get_full_resume()

    prompt = f"""
You are an expert Resume Reviewer.

Analyze the resume and provide:

1. ATS Score (/100)

2. Strengths

3. Weaknesses

4. Missing Skills

5. Resume Improvements

6. Career Recommendations

Resume:
{context}
"""

    response = llm.invoke(prompt)

    return response.content