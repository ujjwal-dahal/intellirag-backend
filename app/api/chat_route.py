from fastapi import APIRouter, HTTPException, status

# Project Imports
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag import generate_rag_answer

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat API"],
)


@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def chat(request: ChatRequest) -> ChatResponse:

    try:
        answer, conversation_id = generate_rag_answer(
            question=request.question, conversation_id=request.conversation_id
        )

        return ChatResponse(
            conversation_id=conversation_id,
            question=request.question,
            answer=answer,
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate answer.",
        ) from error
