from sqlalchemy.orm import Session

# Project Imports
from app.database.models import Document


def save_document_metadata(
    db: Session,
    document_id: str,
    filename: str,
    file_type: str,
    chunking_strategy: str,
    total_chunks: int,
) -> Document:

    document = Document(
        id=document_id,
        filename=filename,
        file_type=file_type,
        chunking_strategy=chunking_strategy,
        total_chunks=total_chunks,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document
