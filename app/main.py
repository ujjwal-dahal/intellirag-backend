from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from pathlib import Path

# Project Imports
from app.api.document_routes import router as document_router
from app.api.chat_route import router as chat_router
from app.database.qdrant import create_doc_collection

BASE_DIR = Path(__file__).resolve().parent


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
app.include_router(chat_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "message": "RAG Backend is running",
    }


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "templates" / "index.html")
