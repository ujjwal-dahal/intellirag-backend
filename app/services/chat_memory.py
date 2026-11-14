import json

# Project Imports
from app.database.redis import redis_client
from app.core.constants import CHAT_HISTORY_LIMIT, CHAT_MEMORY_TTL


def get_chat_history(conversation_id: str):

    # Redis Key of Conversation
    redis_key = f"chat:{conversation_id}"

    messages = redis_client.lrange(redis_key, 0, -1)

    # Booking state lai chat history bata exclude garne
    return [
        data
        for msg in messages
        if (data := json.loads(msg)).get("type") != "booking_state"
    ]


def save_chat_message(conversation_id: str, role: str, content: str):

    redis_key = f"chat:{conversation_id}"

    # Message lai JSON string ma convert gareko
    message = json.dumps({"role": role, "content": content})

    # adding message in Redis List
    redis_client.rpush(redis_key, message)

    # Preserving only Latest 10 Messages

    # Booking state remove nahos bhanera chat messages matra count garne
    messages = redis_client.lrange(redis_key, 0, -1)

    chat_messages = [
        msg for msg in messages if json.loads(msg).get("type") != "booking_state"
    ]

    # Latest chat messages preserve garne
    if len(chat_messages) > CHAT_HISTORY_LIMIT:
        for msg in chat_messages[:-CHAT_HISTORY_LIMIT]:
            redis_client.lrem(redis_key, 1, msg)

    # Expire After 7 Days
    redis_client.expire(redis_key, CHAT_MEMORY_TTL)


def get_booking_state(conversation_id: str) -> dict:

    redis_key = f"chat:{conversation_id}"

    messages = redis_client.lrange(redis_key, 0, -1)

    for message in messages:
        data = json.loads(message)

        if data.get("type") == "booking_state":
            return data.get("data", {})

    return {}


def save_booking_state(
    conversation_id: str,
    booking_data: dict,
) -> None:

    redis_key = f"chat:{conversation_id}"

    messages = redis_client.lrange(redis_key, 0, -1)

    # Existing booking state remove garne
    for message in messages:
        data = json.loads(message)

        if data.get("type") == "booking_state":
            redis_client.lrem(redis_key, 1, message)

    # Booking details lai JSON string ma convert garne
    booking_record = json.dumps(
        {
            "type": "booking_state",
            "data": booking_data,
        }
    )

    # Redis ma booking state save garne
    redis_client.rpush(redis_key, booking_record)

    # Expire After 7 Days
    redis_client.expire(redis_key, CHAT_MEMORY_TTL)


def delete_booking_state(conversation_id: str) -> None:

    redis_key = f"chat:{conversation_id}"

    messages = redis_client.lrange(redis_key, 0, -1)

    # Booking state matra delete garne, chat history haina
    for message in messages:
        data = json.loads(message)

        if data.get("type") == "booking_state":
            redis_client.lrem(redis_key, 1, message)


def has_booking_state(conversation_id: str) -> bool:
    redis_key = f"chat:{conversation_id}"

    for message in redis_client.lrange(redis_key, 0, -1):
        if json.loads(message).get("type") == "booking_state":
            return True

    return False
