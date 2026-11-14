from fastapi import FastAPI

app = FastAPI(
    title="IntelliRAG Backend",
    description="Document-based Conversational RAG System",
    version="1.0.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "message": "RAG Backend is running",
    }
