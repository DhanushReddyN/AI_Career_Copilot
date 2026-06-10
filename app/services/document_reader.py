from app.services.vector_store import load_vector_store

def get_documents(db_path):

    db = load_vector_store(db_path)

    data = db.get()

    docs = data["documents"]

    if not docs:
        return ""

    return "\n\n".join(docs)