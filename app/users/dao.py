import re
from pydantic import EmailStr, Json
from app.dao.base import BaseDAO
from app.database import get_redis_connection






class UserDAO(BaseDAO):
    
    
    
    # метод для добавления пользователя
    @classmethod
    async def add_user(cls, email: EmailStr, data: Json):
        redis_client = await get_redis_connection()

        result = await redis_client.execute_command("SET", email, data)
        
        return "Данные добавлены"
    
    # метод для поиска пользователя
    @classmethod
    async def find_user(cls, email: EmailStr):
        redis_client = await get_redis_connection()

        result = await redis_client.execute_command("GET", email)
        return [email, result.decode("utf-8")] if result else None
    
    
    
    
    # метод для получения количества пользователей
    @classmethod
    async def all_users_count(cls):
        redis_client = await get_redis_connection()
        all_keys = await redis_client.keys('*')
        
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

        all_keys = [key.decode('utf-8') for key in all_keys]

        # Фильтрация ключей, начинающихся с email@
        email_keys = [key for key in all_keys if email_regex.match(key)]
        
        return len(email_keys)