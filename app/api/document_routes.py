from fastapi import APIRouter, File, UploadFile, status, Form, Depends, HTTPException

from typing import Literal
from pathlib import Path
import uuid

# sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Project Imports
from app.schemas.document import DocumentUploadResponse
from app.database.connection import get_db
from app.core.constants import MAX_UPLOAD_SIZE
from app.utils.file_extractor import extract_text
from app.services.ingestion import save_document_metadata
from app.services.chunking import create_chunks
from app.services.embedding import generate_embeddings
from app.services.vector_store import store_chunks

router = APIRouter(prefix="/api/v1/documents", tags=["Document Ingestion API"])


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: Literal["recursive", "semantic"] = Form(...),
    db: Session = Depends(get_db),
) -> DocumentUploadResponse:

    try:

        # Eg : file.filename = "my_pdf.pdf"

        # Checking File Type
        filename = (file.filename or "").replace("\\", "/").split("/")[-1]

        if not filename:
            raise HTTPException(status_code=400, detail="Invalid File Name")

        file_type = Path(filename).suffix.lower().lstrip(".")

        if file_type not in ["pdf", "txt"]:
            raise HTTPException(
                status_code=415, detail="Only PDF and TXT Files are Supported"
            )

        # Checking File Size Limit

        # It reads Maximum Upload Size + 1 Byte
        file_bytes = await file.read(size=MAX_UPLOAD_SIZE + 1)

        if len(file_bytes) > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413, detail="File Size Exceeds the Upload Limit"
            )

        # When File is Empty
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded File is Empty")

        # Now Extracting Document Text
        try:
            extracted_text = extract_text(file_bytes=file_bytes, file_type=file_type)

        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error),
            ) from error

        # Chunks are Converted from Extracted Texts
        chunks = create_chunks(
            texts=extracted_text,
            strategy=chunking_strategy,
        )

        if not chunks:
            raise HTTPException(
                status_code=422,
                detail="No chunks could be generated.",
            )

        # Chunks to Embedding
        embeddings = generate_embeddings(chunks)

        document_id = str(uuid.uuid4())

        # Save Metadata in SQL
        try:

            document = save_document_metadata(
                db=db,
                document_id=document_id,
                filename=filename,
                file_type=file_type,
                chunking_strategy=chunking_strategy,
                total_chunks=len(chunks),
            )

        except SQLAlchemyError as error:

            db.rollback()
            # print("SQLAlchemy Error:", repr(error))
            raise HTTPException(
                status_code=500, detail="Failed to Save Document Metadata"
            ) from error

        try:
            store_chunks(
                document_id=document_id,
                filename=filename,
                chunking_strategy=chunking_strategy,
                chunks=chunks,
                embeddings=embeddings,
            )

        # At first Metadata Should Store in SQLDB and then Vector should Store in Qdrant
        except Exception as error:

            try:
                # If Qdrant fails, delete metadata from Neon
                db.delete(document)
                db.commit()
            except SQLAlchemyError:
                db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to store document vectors.",
            ) from error

        return DocumentUploadResponse(
            document_id=document.id,
            filename=document.filename,
            file_type=document.file_type,
            chunking_strategy=document.chunking_strategy,
            extracted_characters=len(extracted_text),
            total_chunks=document.total_chunks,
            message="Document Uploaded & Text Extracted Successfully",
        )

    finally:
        await file.close()
