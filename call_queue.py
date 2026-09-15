import redis
from rq import Queue

redis_connection = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

call_queue = Queue(
    "calls",
    connection=redis_connection
)