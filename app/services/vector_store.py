import uuid
from qdrant_client import models

# Project Imports
from app.database.qdrant import qd_client
from app.core.constants import COLLECTION_NAME


def store_chunks(
    document_id: str,
    filename: str,
    chunking_strategy: str,
    chunks: list[str],
    embeddings,
):

    points = []

    # Creating Vector Record for Each Chunk
    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

        point = models.PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding.tolist(),
            payload={
                "document_id": document_id,
                "filename": filename,
                "chunking_index": index,
                "chunking_strategy": chunking_strategy,
                "text": chunk,
            },
        )

        points.append(point)

    # Storing All Points to Vector Store
    qd_client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
