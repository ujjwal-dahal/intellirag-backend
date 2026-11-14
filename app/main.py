from fastapi import FastAPI

# Project Imports
from app.api.document_routes import router as document_router

app = FastAPI(
    title="IntelliRAG Backend",
    description="Document-based Conversational RAG System",
    version="1.0.0",
)

# Registering Router
app.include_router(document_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "message": "RAG Backend is running",
    }
