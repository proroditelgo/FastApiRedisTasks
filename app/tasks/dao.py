import json
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
    async def get_all_tasks_count(cls, user_id: int):
        
        redis_client = await get_redis_connection()
        keys = await redis_client.keys(f"{user_id}*")
        
        return len(keys)
    
    
    # метод для выгрузки всех задачs
    @classmethod
    async def get_all_user_tasks(cls, user_id: int, task_count: int, task_viewed: int):
        
        end_of_data = False
        
        dict_values = []
        
        # перебор задач, в зависимости от заданного количества отображения 
        for task in range(task_count):
            task +=1
            
            values = await cls.find_one(key = f'{user_id}_{int(task)+int(task_viewed)}')
            
            if values:
                dict_values.append(
                    json.loads(values)
                    )
                continue
            
            else:
                end_of_data = True
                break

        
        
        
        return [dict_values, end_of_data]
    
    
    
    # метод для поиска свободного номера для задачи
    @classmethod
    async def get_free_task_number(cls, user_id: int):
        
        redis_client = await get_redis_connection()
        keys = await redis_client.keys(f"{user_id}*")

        print(len(keys))
        
        task_number = 1
        
        
        if len(keys) == 0:
            return task_number
        
        
        for key in keys:
            if key.decode("utf-8") == f"{user_id}_{task_number}":
                print(f"Не туда {task_number}")
                return task_number
            else:
                print(task_number)
                task_number += 1
    
