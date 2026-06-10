from app.services.document_reader import get_documents
from app.services.llm_service import get_llm_smart

llm = get_llm_smart()

def generate_interview_questions():

    resume_text = get_documents(
        "./chroma_resume"
    )

    prompt = f"""
You are a senior technical interviewer.

Analyze the candidate's resume.

Generate highly personalized interview questions.

Rules:

- Questions must be based on the candidate's actual resume.
- Focus on projects, skills and experience.
- Avoid generic textbook questions.
- Ask questions that a real interviewer would ask.

Generate:

SECTION 1:
Resume-Based Questions (5)

SECTION 2:
Project-Based Questions (5)

SECTION 3:
Technical Questions (5)

SECTION 4:
Scenario-Based Questions (5)

SECTION 5:
HR Questions (5)

SECTION 6:
Follow-up Questions (5)

Return only questions.

Resume:
{resume_text}
"""

    response = llm.invoke(prompt)

    return response.content