#app/services/redis_client.py
import redis
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# Parse Redis URL from environment variable
redis_url = (
    os.getenv("REDIS_URL") or
    os.getenv("REDISCLOUD_URL") or
    "redis://localhost:6379"
)
parsed_url = urlparse(redis_url)

# Initialize Redis client
r = redis.Redis(
    host=parsed_url.hostname,
    port=parsed_url.port,
    password=parsed_url.password,
    decode_responses=True
)

def init_progress(task_id: str, models: list[str], total: int):
    """Initialize progress counters for each model."""
    for model in models:
        r.hset(f"analyze_progress:{task_id}", model, 0)
    r.hset(f"analyze_progress:{task_id}", "total", total)

def increment_progress(task_id: str, model: str):
    """Increment progress for a specific model."""
    r.hincrby(f"analyze_progress:{task_id}", model, 1)

def get_progress(task_id: str) -> dict:
    """Retrieve current progress data."""
    return r.hgetall(f"analyze_progress:{task_id}")
