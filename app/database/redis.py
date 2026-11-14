from upstash_redis import Redis

# project imports
from app.core.config import settings

"""Redis Client"""
redis_client = Redis(
    url=settings.redis_rest_url,
    token=settings.redis_rest_token,
)

"""To Check Connection"""


def check_redis_connection() -> bool:
    try:
        return redis_client.ping()
    except Exception:
        return False
