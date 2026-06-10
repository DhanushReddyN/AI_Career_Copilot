from app.services.document_reader import get_documents
from app.services.llm_service import get_llm_smart

llm = get_llm_smart()

def generate_learning_roadmap():

    resume_text = get_documents(
        "./chroma_resume"
    )

    jd_text = get_documents(
        "./chroma_jd"
    )

    prompt = f"""
You are an expert AI Career Coach.

Your task:

1. Compare the resume with the job description.
2. Identify missing skills.
3. Create a practical 6-month learning roadmap.

Rules:

- Do NOT explain the resume.
- Do NOT explain the job description.
- Do NOT provide analysis.
- Do NOT provide match percentage.
- Focus ONLY on missing skills.
- Start directly with Month 1.
- Each month must contain:
    - Skills
    - Resources
    - Project

Prioritize these skills if missing:

1. Docker
2. AWS
3. Kubernetes
4. CI/CD
5. LangChain
6. RAG
7. Vector Databases
8. LLM Applications

Output Format:

Month 1:
Skills:
Resources:
Project:

Month 2:
Skills:
Resources:
Project:

Month 3:
Skills:
Resources:
Project:

Month 4:
Skills:
Resources:
Project:

Month 5:
Skills:
Resources:
Project:

Month 6:
Skills:
Resources:
Project:

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = llm.invoke(prompt)

    return response.content