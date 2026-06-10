from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os

from app.services.document_loader import load_pdf
from app.services.document_reader import get_documents
from app.services.document_reader import get_documents
from app.services.text_splitter import create_chunks
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import (
    create_vector_store,
    load_vector_store
)
from app.services.retriever_service import retrieve_chunks
from app.services.rag_service import ask_resume
from app.services.resume_analyzer import analyze_resume
from app.services.match_service import calculate_match_score
from app.services.skill_gap_service import analyze_skill_gap
from app.services.roadmap_service import (
    generate_learning_roadmap
)
from app.services.interview_service import (
    generate_interview_questions
)
from app.services.interview_prep_service import (
    generate_interview_prep
)
from app.services.career_agent import career_coach


router = APIRouter()

UPLOAD_DIR = "app/data/resumes"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# --------------------------------------------------
# Upload Resume
# --------------------------------------------------

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    # Reset pointer so we always read the full file content
    await file.seek(0)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = load_pdf(file_path)

    chunks = create_chunks(docs)

    print("TOTAL CHUNKS:", len(chunks))

    # create_vector_store now deletes the old collection internally,
    # so we no longer need to rmtree the folder here. Keeping the
    # folder avoids issues when another request is reading it.
    create_vector_store(
        chunks,
        persist_directory="./chroma_resume"
    )

    print("RESUME VECTOR DB CREATED")

    return {
        "message": "Resume uploaded successfully",
        "chunks": len(chunks)
    }
# --------------------------------------------------
# Test Embeddings
# --------------------------------------------------

@router.post("/test-embeddings")
async def test_embeddings(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = load_pdf(file_path)

    chunks = create_chunks(docs)

    embeddings = generate_embeddings(chunks)

    return {
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "sample_vector": embeddings[0][:10].tolist()
    }


# --------------------------------------------------
# Create Vector DB
# --------------------------------------------------

@router.post("/create-vector-db")
async def create_db(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = load_pdf(file_path)

    chunks = create_chunks(docs)

    create_vector_store(
        chunks,
        persist_directory="./chroma_resume"
    )

    return {
        "message": "Vector DB created successfully",
        "chunks_stored": len(chunks)
    }


# --------------------------------------------------
# Search Resume
# --------------------------------------------------

@router.post("/search-resume")
async def search_resume(
    question: str = Form(...)
):

    results = retrieve_chunks(question)

    return {
        "question": question,
        "retrieved_chunks": [
            doc.page_content
            for doc in results
        ]
    }


# --------------------------------------------------
# Ask Resume (RAG)
# --------------------------------------------------

@router.post("/ask-resume")
async def ask_resume_api(
    question: str = Form(...)
):

    answer = ask_resume(question)

    return {
        "question": question,
        "answer": answer
    }


# --------------------------------------------------
# Resume Analysis
# --------------------------------------------------

@router.get("/analyze-resume")
async def analyze_resume_api():
    try:
        result = analyze_resume()
        return {"analysis": result}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str or "429" in error_str:
            raise HTTPException(status_code=503, detail=error_str)
        raise


# --------------------------------------------------
# Resume-JD Match Score
# --------------------------------------------------

@router.get("/match-score")
async def match_score_api():

    result = calculate_match_score()

    return result


# --------------------------------------------------
# Skill Gap Analysis
# --------------------------------------------------

@router.get("/skill-gap")
async def skill_gap_api():
    try:
        result = analyze_skill_gap()
        return {"analysis": result}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str or "429" in error_str:
            raise HTTPException(status_code=503, detail=error_str)
        raise


# --------------------------------------------------
# Debug Endpoint
# --------------------------------------------------

@router.get("/debug-db")
async def debug_db():

    resume_db = load_vector_store(
        "./chroma_resume"
    )

    jd_db = load_vector_store(
        "./chroma_jd"
    )

    return {
        "resume_docs": len(
            resume_db.get()["documents"]
        ),
        "jd_docs": len(
            jd_db.get()["documents"]
        )
    }

# --------------------------------------------------
# Learning Roadmap

@router.get("/learning-roadmap")
async def learning_roadmap_api():
    try:
        result = generate_learning_roadmap()
        return {"roadmap": result}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str or "429" in error_str:
            raise HTTPException(status_code=503, detail=error_str)
        raise


@router.get("/interview-questions")
async def interview_questions_api():
    try:
        result = generate_interview_questions()
        return {"questions": result}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str or "429" in error_str:
            raise HTTPException(status_code=503, detail=error_str)
        raise


@router.get("/interview-prep")
async def interview_prep_api():
    try:
        result = generate_interview_prep()
        return {"interview_prep": result}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str or "429" in error_str:
            raise HTTPException(status_code=503, detail=error_str)
        raise


@router.post("/career-coach")
async def career_coach_api(
    question: str = Form(...)
):

    result = career_coach(question)

    return {
        "response": result
    }

@router.get("/debug-resume")
async def debug_resume():

    docs = get_documents("./chroma_resume")

    return {
        "chunks": len(docs),
        "sample": docs[:5]
    }