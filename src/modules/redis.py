import redis
import os

class Redis:
    def __init__(self):
        self.redis = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)

    def write(self, key: str, value: str) -> None:
        self.redis.set(key, value)

    def read(self, key: str) -> str:
        return self.redis.get(key)