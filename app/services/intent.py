from typing import Literal
import json

# Project Imports
from app.services.llm import get_groq_client


def detect_chat_intent(
    message: str,
    booking_in_progress: bool = False,
) -> Literal["rag", "booking"]:

    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an intent classification assistant. "
                    "Classify the user's message into exactly one intent: "
                    "'rag' or 'booking'. "
                    "Use 'booking' when the user wants to start, schedule, "
                    "book, modify, confirm, or cancel an interview appointment. "
                    "Use 'rag' for questions about documents, company "
                    "information, existing interview records, or other "
                    "general queries. "
                    "Classify questions such as 'Has he booked an interview?', "
                    "'When is his interview?', and 'Does Ujjwal have an interview?' "
                    "as 'rag'. "
                    "If the user provides personal details such as their name, "
                    "email, preferred interview date, or time, classify as "
                    "'booking' when the message is clearly part of an interview "
                    "booking conversation. "
                    "A short reply containing only a name, email, date, or time "
                    "should be classified as 'booking' when a booking conversation "
                    "is already in progress. "
                    "Do not classify general questions as booking just because "
                    "they mention an interview. "
                    "Return only a valid JSON object with exactly this key: "
                    '{"intent": "rag" or "booking"}.'
                    f"Booking conversation in progress: {booking_in_progress}."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response.")

    data = json.loads(content)

    intent = data.get("intent")

    if intent not in {"rag", "booking"}:
        raise ValueError("Groq returned an invalid intent.")

    return intent
