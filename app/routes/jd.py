from fastapi import APIRouter, UploadFile, File
import os
import shutil

from app.services.document_loader import load_pdf
from app.services.text_splitter import create_chunks
from app.services.vector_store import create_vector_store

router = APIRouter()

JD_DIR = "app/data/jds"

os.makedirs(JD_DIR, exist_ok=True)

@router.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)):

    file_path = os.path.join(
        JD_DIR,
        file.filename
    )

    # Reset pointer so we always read the full file content
    await file.seek(0)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = load_pdf(file_path)

    chunks = create_chunks(docs)

    # create_vector_store now deletes the old collection internally
    create_vector_store(
        chunks,
        persist_directory="./chroma_jd"
    )

    return {
        "message": "JD uploaded successfully"
    }

@router.get("/jd-test")
def jd_test():
    return {"message": "JD route working"}