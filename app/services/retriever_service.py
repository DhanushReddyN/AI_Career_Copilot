from app.services.vector_store import load_vector_store

def retrieve_chunks(query):

    db = load_vector_store("./chroma_resume")

    results = db.similarity_search(
        query=query,
        k=3
    )

    return results