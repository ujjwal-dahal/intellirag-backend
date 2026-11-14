import json
from datetime import datetime
from zoneinfo import ZoneInfo

# Project Imports
from app.services.llm import get_groq_client


def extract_booking_details(
    message: str,
):

    client = get_groq_client()

    # Nepal ko current date retrieve garne
    today = datetime.now(ZoneInfo("Asia/Kathmandu")).date().isoformat()

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Today's date is {today}. "
                    "Resolve relative dates like 'tomorrow', "
                    "'day after tomorrow', or 'next Monday' "
                    "using today's date. "
                    "You are a booking information extraction assistant. "
                    "Extract only the booking details explicitly provided "
                    "in the user's latest message. "
                    "Do not guess or invent missing information. "
                    "Return null for any missing field. "
                    "Return interview_date in YYYY-MM-DD format only "
                    "when the full date is clear. "
                    "Return interview_time in 24-hour HH:MM format "
                    "only when the time is clear. "
                    "If the date or time is ambiguous, return null. "
                    "Return a valid JSON object with exactly these keys: "
                    "name, email, interview_date, interview_time."
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

    return {
        "name": data.get("name"),
        "email": data.get("email"),
        "interview_date": data.get("interview_date"),
        "interview_time": data.get("interview_time"),
    }
