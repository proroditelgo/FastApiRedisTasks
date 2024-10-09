from pydantic import EmailStr
from app.dao.base import BaseDAO
from app.database import get_redis_connection






class UserDAO(BaseDAO):
    
    
    
    # метод для добавления пользователя
    @classmethod
    async def add_user(cls, email: EmailStr, hashed_password: str):
        redis_client = await get_redis_connection()

        result = await redis_client.execute_command("SET", email, hashed_password)
        
        return "Данные добавлены"
    
    # метод для поиска пользователя
    @classmethod
    async def find_user(cls, email: EmailStr):
        redis_client = await get_redis_connection()

        result = await redis_client.execute_command("GET", email)
        return [email, result.decode("utf-8")] if result else None