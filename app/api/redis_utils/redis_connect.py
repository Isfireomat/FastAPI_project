import os
from typing import AsyncGenerator
from redis.asyncio import Redis
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_redis_client() -> AsyncGenerator[Redis, None]:
    client: Redis = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)
    try:
        yield client
    finally:
        await client.close() 

async def get_client() -> Redis:
    async with get_redis_client() as client:
        yield client  