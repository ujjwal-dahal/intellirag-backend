from fastapi import FastAPI
from contextlib import asynccontextmanager

# Project Imports
from app.api.document_routes import router as document_router
from app.database.qdrant import create_doc_collection


# Creating Collection during Start of FastAPI App
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before App Start
    create_doc_collection()

    yield


app = FastAPI(
    title="IntelliRAG Backend",
    description="Document-based Conversational RAG System",
    version="1.0.0",
    lifespan=lifespan,
)

# Registering Router
app.include_router(document_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "message": "RAG Backend is running",
    }
