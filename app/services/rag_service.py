from app.services.retriever_service import retrieve_chunks
from app.services.llm_service import get_llm_smart

llm = get_llm_smart()

def ask_resume(question):

    docs = retrieve_chunks(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an expert AI Career Assistant.

Answer the user's question based ONLY on the resume context.

Rules:
1. Give concise and professional answers.
2. Use bullet points whenever appropriate.
3. Do not invent information.
4. If information is missing, say:
   'Information not found in resume.'
Resume Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content