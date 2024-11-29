from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# для кеширования
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

# роутеры
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router

from app.config import settings


app = FastAPI()


app.include_router(users_router)
app.include_router(tasks_router)
  

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "DELETE", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)  
  
# для кеширования с временем сохранения кеша 
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
	redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", 
        encoding="utf8", 
        decode_responses=True
        )
 
	FastAPICache.init(RedisBackend(redis), prefix="cache")
	yield
 
 
 