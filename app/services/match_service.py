from sklearn.metrics.pairwise import cosine_similarity

from app.services.vector_store import load_vector_store
from app.services.embedding_service import embedding_model

def calculate_match_score():

    resume_db = load_vector_store("./chroma_resume")
    jd_db = load_vector_store("./chroma_jd")

    resume_docs = resume_db.get()
    jd_docs = jd_db.get()

    resume_text = " ".join(
        resume_docs["documents"]
    )

    jd_text = " ".join(
        jd_docs["documents"]
    )

    resume_embedding = embedding_model.embed_query(
        resume_text
    )

    jd_embedding = embedding_model.embed_query(
        jd_text
    )

    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    match_score = round(
        similarity * 100,
        2
    )

    return {
        "match_score": match_score,
        "similarity": float(similarity)
    }