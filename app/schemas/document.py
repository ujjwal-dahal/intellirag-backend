from pydantic import BaseModel, ConfigDict

"""After Uploading Document , Response of API"""


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    file_type: str
    chunking_strategy: str
    extracted_characters: int
    total_chunks: int

    message: str

    model_config = ConfigDict(
        from_attributes=True,
    )
