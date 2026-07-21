import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_huggingface import HuggingFaceEmbeddings

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embedding_model

# Collection names used by resume and JD stores
RESUME_COLLECTION = "resume_collection"
JD_COLLECTION = "jd_collection"


def _get_chroma_settings():
    """Return ChromaDB settings that allow reset (force-flush of old data)."""
    return Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )


def create_vector_store(chunks, persist_directory):
    """
    Create a fresh Chroma vector store from the given chunks.
    Resets any existing collection so stale data from a previous
    upload is never returned.
    """
    # Determine collection name from directory path
    if "chroma_resume" in persist_directory:
        collection_name = RESUME_COLLECTION
    elif "chroma_jd" in persist_directory:
        collection_name = JD_COLLECTION
    else:
        collection_name = "default_collection"

    # Create a persistent client that supports reset
    client = chromadb.PersistentClient(
        path=persist_directory,
        settings=_get_chroma_settings()
    )

    # Delete the old collection if it exists so we start fresh
    existing = [c.name for c in client.list_collections()]
    if collection_name in existing:
        client.delete_collection(collection_name)

    # Build the LangChain Chroma wrapper with the fresh client
    db = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=get_embedding_model(),
    )

    # Add documents
    db.add_documents(chunks)

    return db


def load_vector_store(persist_directory):
    """
    Load an existing Chroma vector store.
    Always creates a new client so we never read from a stale
    in-memory cache.
    """
    if "chroma_resume" in persist_directory:
        collection_name = RESUME_COLLECTION
    elif "chroma_jd" in persist_directory:
        collection_name = JD_COLLECTION
    else:
        collection_name = "default_collection"

    client = chromadb.PersistentClient(
        path=persist_directory,
        settings=_get_chroma_settings()
    )

    db = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=get_embedding_model(),
    )

    return db