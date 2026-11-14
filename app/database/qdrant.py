from qdrant_client import QdrantClient, models

# project imports
from app.core.config import settings
from app.core.constants import COLLECTION_NAME, VECTOR_SIZE, M, EF_CONSTRUCT

"""Qdrant Client"""
qd_client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key,
)

"""To Check Qdrant Connection"""


def check_qdrant_connection() -> bool:
    try:
        qd_client.get_collections()
        return True
    except Exception:
        return False


"""Creating Collection"""


def create_doc_collection():

    # Collection already Exist then Exit i.e no need to recreate
    if qd_client.collection_exists(COLLECTION_NAME):
        return

    qd_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE, distance=models.Distance.COSINE
        ),
        # HNSW (Hierarchical Navigable Small World) Indexing Configuration
        hnsw_config=models.HnswConfigDiff(m=M, ef_construct=EF_CONSTRUCT),
    )
