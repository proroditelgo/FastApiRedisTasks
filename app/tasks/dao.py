import re
from pydantic import EmailStr, Json
from app.dao.base import BaseDAO
from app.database import get_redis_connection






class TaskDAO(BaseDAO):
    
    
    
    
    # метод для добавления задачи
    @classmethod
    async def add_task(cls, data: Json, task_id: int, user_id: int):
        redis_client = await get_redis_connection()
        
        task_name = f"{user_id}_{task_id}"
        
        result = await redis_client.execute_command("SET", task_name, data)
        
        return "Данные добавлены"
    
    
    
    
    # метод для получения количества задач
    @classmethod
    async def all_tasks_count(cls, user_id: int):
        
        redis_client = await get_redis_connection()
        all_keys = await redis_client.keys('*')
        
        
        email_regex = re.compile(f"{user_id}_")

        all_keys = [key.decode('utf-8') for key in all_keys]

        # фильтрация по номеру пользователя, ключи задач в формате user_id + task_id
        email_keys = [key for key in all_keys if email_regex.match(key)]
        
        return len(email_keys)