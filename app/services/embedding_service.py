from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    return _model

def generate_embeddings(chunks):
    texts = [chunk.page_content for chunk in chunks]
    model = get_model()
    return model.encode(texts)