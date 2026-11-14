from pydantic import ValidationError
from datetime import date, time, datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


from app.services.chat_memory import (
    get_booking_state,
    save_booking_state,
    delete_booking_state,
)
from app.services.booking_llm import extract_booking_details
from app.core.constants import REQUIRED_BOOKING_FIELDS
from app.schemas.booking import BookingDetails
from app.database.models import InterviewBooking


def collect_booking_details(
    conversation_id: str,
    message: str,
):

    # Redis bata existing booking details retrieved
    booking_data = get_booking_state(
        conversation_id=conversation_id,
    )

    # Groq bata current message ko details extracted
    extracted_data = extract_booking_details(
        message=message,
    )

    # New non-empty details le existing data update garne
    for field, value in extracted_data.items():
        if value is not None:
            booking_data[field] = value

    # Updated booking details Redis ma save garne
    save_booking_state(
        conversation_id=conversation_id,
        booking_data=booking_data,
    )

    # Missing booking fields identify
    missing_fields = [
        field for field in REQUIRED_BOOKING_FIELDS if not booking_data.get(field)
    ]

    return booking_data, missing_fields


def validate_booking_details(
    booking_data: dict,
) -> tuple[BookingDetails | None, dict[str, str]]:
    try:
        validated_data = BookingDetails(**booking_data)
        return validated_data, {}

    except ValidationError as error:
        errors = {item["loc"][0]: item["msg"] for item in error.errors() if item["loc"]}

        return None, errors


def get_next_booking_question(
    missing_fields: list[str],
) -> str:

    # Missing field anusar question define garne
    questions = {
        "name": "Please provide your full name.",
        "email": "Please provide your email address.",
        "interview_date": "Which date would you prefer for the interview?",
        "interview_time": "What time would you prefer for the interview?",
    }

    # First missing field ko question return garne
    if missing_fields:
        return questions[missing_fields[0]]

    return "All booking details have been collected."


def get_invalid_field_question(
    field: str,
) -> str:

    questions = {
        "name": "Please provide a valid full name.",
        "email": "The email address is invalid. Please provide a valid email.",
        "interview_date": "The interview date is invalid or in the past. Please provide a future date.",
        "interview_time": "The interview time is invalid. Please provide a valid time.",
    }

    return questions.get(
        field,
        "Please provide valid booking information.",
    )


def process_booking_message(
    conversation_id: str,
    message: str,
):

    booking_data = get_booking_state(conversation_id)

    # User confirmation handle garne
    if booking_data.get("awaiting_confirmation"):

        user_reply = message.strip().lower()

        if user_reply in {"yes", "y", "confirm", "confirmed"}:
            booking_data.pop("awaiting_confirmation")

            save_booking_state(
                conversation_id=conversation_id,
                booking_data=booking_data,
            )

            return (
                "Your booking details are confirmed.",
                True,
                booking_data,
            )

        if user_reply in {"no", "n", "cancel"}:
            delete_booking_state(conversation_id)

            return (
                "Booking cancelled. You can start a new booking.",
                False,
                {},
            )

        return (
            "Please reply with yes or no to confirm your booking.",
            False,
            booking_data,
        )

    # User message bata booking details collect garne
    booking_data, missing_fields = collect_booking_details(
        conversation_id=conversation_id,
        message=message,
    )

    # Missing details check garne
    if missing_fields:
        reply = get_next_booking_question(missing_fields)

        return reply, False, booking_data

    # All details validate garne
    validated_data, errors = validate_booking_details(
        booking_data=booking_data,
    )

    # Invalid details handle garne
    if errors:
        for field in errors:
            booking_data.pop(field, None)

        save_booking_state(
            conversation_id=conversation_id,
            booking_data=booking_data,
        )

        invalid_field = next(iter(errors))

        reply = get_invalid_field_question(invalid_field)

        return reply, False, booking_data

    # User bata final confirmation magne
    booking_data["awaiting_confirmation"] = True

    save_booking_state(
        conversation_id=conversation_id,
        booking_data=booking_data,
    )

    reply = (
        "Please confirm your interview booking details:\n"
        f"Name: {validated_data.name}\n"
        f"Email: {validated_data.email}\n"
        f"Date: {validated_data.interview_date.isoformat()}\n"
        f"Time: {validated_data.interview_time.strftime('%H:%M')}\n\n"
        "Reply yes to confirm or no to cancel."
    )

    return reply, False, booking_data


def save_interview_booking(
    db: Session,
    booking_data: dict,
) -> InterviewBooking:

    interview_date = date.fromisoformat(booking_data["interview_date"])

    interview_time = time.fromisoformat(booking_data["interview_time"])

    interview_datetime = datetime.combine(
        interview_date,
        interview_time,
        tzinfo=ZoneInfo("Asia/Kathmandu"),
    )

    booking = InterviewBooking(
        name=booking_data["name"],
        email=booking_data["email"],
        interview_date=interview_datetime,
    )

    try:
        # Database ma booking add garne
        db.add(booking)

        # Database ma permanently save garne
        db.commit()

        # Database bata updated object retrieve garne
        db.refresh(booking)

        return booking

    except SQLAlchemyError:
        # Error aaye transaction rollback garne
        db.rollback()
        raise
