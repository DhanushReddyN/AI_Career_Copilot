from app.services.document_reader import get_documents
from app.services.llm_service import get_llm_smart

llm = get_llm_smart()

def generate_interview_prep():

    resume_text = get_documents(
        "./chroma_resume"
    )

    prompt = f"""
You are a Senior Software Engineer and Technical Interviewer.

Analyze the candidate's resume.

Generate interview preparation material.

IMPORTANT:

For each question provide:

1. QUESTION
2. IDEAL ANSWER (write the actual answer as if the candidate is answering)
3. FOLLOW-UP QUESTION
4. KEY POINTS INTERVIEWER EXPECTS

Rules:

- Write complete answers.
- Do NOT write:
    'The candidate should explain...'
    'The candidate should describe...'
- Write answers in first person:
    'I implemented...'
    'I used...'
    'I chose...'
- Focus heavily on candidate projects.
- Generate realistic placement interview questions.

Generate 10 questions.

Resume:
{resume_text}
"""

    response = llm.invoke(prompt)

    return response.content