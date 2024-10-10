from fastapi import FastAPI

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from app.config import settings

# роутеры
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router


app = FastAPI()


app.include_router(users_router)
app.include_router(tasks_router)
  
  
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
	redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", 
        encoding="utf8", 
        decode_responses=True
        )
 
	FastAPICache.init(RedisBackend(redis), prefix="cache")
	yield