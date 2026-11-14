from qdrant_client import models

# Project Imports
from app.database.qdrant import qd_client
from app.services.embedding import generate_embeddings
from app.core.constants import COLLECTION_NAME, HNSW_EF


def retrieve_chunks(
    query: str,
    limit: int = 5,
):

    # Embedding of User Question
    query_embedding = generate_embeddings([query])[0].tolist()

    # Qdrant bata relevant chunks retrieve garne
    search_result = qd_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        search_params=models.SearchParams(
            hnsw_ef=HNSW_EF,
            exact=False,
        ),
    )

    # Retrieved chunks bata text extract garne
    chunks = [
        point.payload["text"]
        for point in search_result.points
        if point.payload and point.payload.get("text")
    ]

    return chunks
