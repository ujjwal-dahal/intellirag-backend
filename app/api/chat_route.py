from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import uuid

# Project Imports
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag import generate_rag_answer
from app.services.intent import detect_chat_intent
from app.services.booking import (
    process_booking_message,
    save_interview_booking,
)
from app.services.chat_memory import (
    has_booking_state,
    delete_booking_state,
    save_booking_state,
)
from app.database.connection import get_db

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat API"],
)


@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:

    try:

        conversation_id = request.conversation_id

        # User ko intent detect garne
        intent = detect_chat_intent(message=request.question)

        # Existing booking conversation checking
        booking_in_progress = conversation_id and has_booking_state(conversation_id)

        # Booking state active cha bhane booking-related short replies continue garne
        if booking_in_progress and intent == "booking":
            intent = "booking"

        # Booking flow
        if intent == "booking":

            # Conversation ID create garne
            conversation_id = conversation_id or str(uuid.uuid4())

            reply, confirmed, booking_data = process_booking_message(
                conversation_id=conversation_id,
                message=request.question,
            )

            # User le booking confirm garepachi database ma save garne
            if confirmed:

                try:
                    save_interview_booking(
                        db=db,
                        booking_data=booking_data,
                    )

                    # Database ma save bhayepachi Redis state delete garne
                    delete_booking_state(conversation_id)

                    reply = "Your interview booking has been successfully confirmed."

                except SQLAlchemyError:

                    # Database error aaye confirmation state restore garne
                    booking_data["awaiting_confirmation"] = True

                    save_booking_state(
                        conversation_id=conversation_id,
                        booking_data=booking_data,
                    )

                    raise

            return ChatResponse(
                conversation_id=conversation_id,
                question=request.question,
                answer=reply,
            )

        # RAG flow
        answer, conversation_id = generate_rag_answer(
            question=request.question,
            conversation_id=conversation_id,
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
