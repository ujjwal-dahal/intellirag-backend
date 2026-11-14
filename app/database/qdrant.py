from qdrant_client import QdrantClient, models

# project imports
from app.core.config import settings

COLLECTION_NAME = "rag-documents"

# all-MiniLM-L6-v2 embedding dimension
VECTOR_SIZE = 384


"""Qdrant Client"""
qdrant_client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key,
)

"""To Check Qdrant Connection"""


def check_qdrant_connection() -> bool:
    try:
        qdrant_client.get_collections()
        return True
    except Exception:
        return False


"""Creating Collection"""


def create_doc_collection():

    # Collection already Exist then Exit i.e no need to recreate
    if qdrant_client.collection_exists(COLLECTION_NAME):
        return

    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE, distance=models.Distance.COSINE
        ),
        # HNSW (Hierarchical Navigable Small World) Indexing Configuration
        hnsw_config=models.HnswConfigDiff(m=16, ef_construct=100),
    )
