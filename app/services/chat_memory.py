import json

# Project Imports
from app.database.redis import redis_client
from app.core.constants import CHAT_HISTORY_LIMIT, CHAT_MEMORY_TTL


def get_chat_history(conversation_id: str):

    # Redis Key of Conversation
    redis_key = f"chat:{conversation_id}"

    messages = redis_client.lrange(redis_key, 0, -1)

    return [json.loads(msg) for msg in messages]


def save_chat_message(conversation_id: str, role: str, content: str):

    redis_key = f"chat:{conversation_id}"

    # Message lai JSON string ma convert gareko
    message = json.dumps({"role": role, "content": content})

    # adding message in Redis List
    redis_client.rpush(redis_key, message)

    # Preserving only Latest 10 Messages

    redis_client.ltrim(redis_key, -CHAT_HISTORY_LIMIT, -1)

    # Expire After 7 Days
    redis_client.expire(redis_key, CHAT_MEMORY_TTL)
