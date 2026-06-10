from app.services.document_reader import get_documents
from app.services.llm_service import get_llm_smart

llm = get_llm_smart()

def analyze_skill_gap():

    resume_text = get_documents(
        "./chroma_resume"
    )

    jd_text = get_documents(
        "./chroma_jd"
    )

    prompt = f"""
You are an expert technical recruiter.

Compare the resume and job description.

Return:

1. Match Percentage

2. Matched Skills

3. Missing Skills

4. Recommendations

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = llm.invoke(prompt)

    return response.content