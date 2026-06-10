from app.services.vector_store import load_vector_store

def get_full_resume():

    db = load_vector_store("./chroma_resume")

    docs = db.get()

    texts = docs["documents"]

    return "\n\n".join(texts)