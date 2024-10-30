from redis.asyncio import Redis
from typing import Optional, List

async def set_pictures(client: Redis, key: str, pictures: list, time: int=20):
    """
    Запись в кеш картинок на некоторое время
    """ 
    client.set(key,pictures,ex=time)

async def get_pictures(client: Redis, key: str) -> Optional[List]:
    """
    Получение картинок из кеша, если они там есть
    """
    if not await client.exists(key): return None
    pictures: list = await client.get(key)
    return pictures

async def set_picture(client: Redis, key: str|bytes, 
                      picture_and_plagiat_picture: list, time: int=20):
    """
    Запись результата картинки в кеш на время
    """
    client.set(key,picture_and_plagiat_picture,ex=time)

async def get_picture_result(client: Redis, key: str|bytes) -> Optional[List]:
    """
    Получение результатов картинки
    """
    if not await client.exists(key): return None
    result: list = await client.get(key)
    return result
