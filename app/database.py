from redis.asyncio import Redis


from app.config import settings



async def get_redis_connection():
    redis_client = await Redis(
        host=settings.REDIS_HOST, 
        port=settings.REDIS_PORT,
        db=0,
    )
    return redis_client