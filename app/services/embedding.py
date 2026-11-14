from functools import lru_cache

from sentence_transformers import SentenceTransformer

# Project Imports
from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    # Embedding model ek patak load garera reuse garne
    return SentenceTransformer(settings.embedding_model)


def generate_embeddings(texts: list[str]):

    # Multiple Chunks ko Embeddings Generate garne
    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    return embeddings
