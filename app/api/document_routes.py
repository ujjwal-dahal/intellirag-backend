from fastapi import APIRouter, File, UploadFile, status, Form, Depends, HTTPException

from typing import Literal

# sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Project Imports
from app.schemas.document import DocumentUploadResponse
from app.database.connection import get_db
from app.core.config import settings
from app.utils.file_extractor import extract_text
from app.services.ingestion import save_document_metadata

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
        file_type = file.filename.split(".")[-1]

        if file_type not in ["pdf", "txt"]:
            raise HTTPException(
                status_code=415, detail="Only PDF and TXT Files are Supported"
            )

        # Checking File Size Limit

        # It reads Maximum Upload Size + 1 Byte
        file_bytes = await file.read(size=settings.max_upload_size + 1)

        if len(file_bytes) > settings.max_upload_size:
            raise HTTPException(
                status_code=413, detail="File Size Exceeds the 15 MB Limit"
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

        # Save Metadata in SQL
        try:

            document = save_document_metadata(
                db=db,
                filename=file.filename,
                file_type=file_type,
                chunking_strategy=chunking_strategy,
            )

        except SQLAlchemyError as error:

            db.rollback()
            raise HTTPException(
                status_code=500, detail="Failed to Save Document Metadata"
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
