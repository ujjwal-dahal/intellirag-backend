from sqlalchemy.orm import Session

# Project Imports
from app.database.models import Document


def save_document_metadata(
    db: Session,
    filename: str,
    file_type: str,
    chunking_strategy: str,
) -> Document:

    document = Document(
        filename=filename,
        file_type=file_type,
        chunking_strategy=chunking_strategy,
        total_chunks=0,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document
