from functools import lru_cache

from sentence_transformers import SentenceTransformer

# Project Imports
from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    # Embedding model ek patak load garera reuse garne
    return SentenceTransformer(settings.embedding_model)
