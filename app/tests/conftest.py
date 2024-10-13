import json
import pytest
from redis.asyncio import Redis

# для теста эндпоинтов без запуска uvicorn
from httpx import ASGITransport, AsyncClient


from app.config import settings
from app.main import app as fastapi_app




@pytest.fixture
async def redis_client():
    redis_client = await Redis(
        host=settings.REDIS_HOST, 
        port=settings.REDIS_PORT,
        db=0,
    )
    
    yield redis_client
    

    
    
    
# асинхронный клиент
@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac
    
    


# создание клиента с токеном аутентификации  
@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        await ac.post("auth/login", json={
            "email": "test@test.com",
            "password": "test",
        })
        
        assert ac.cookies["user_access_token"]
        yield ac