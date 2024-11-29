from app.database import get_redis_connection
from app.exceptions import RedisConnectionError





class BaseDAO:
    
    # метод для получения данных по почте
    @classmethod
    async def find_one(cls, key: str):
        redis_client = await get_redis_connection()

        result = await redis_client.execute_command("GET", key)
        return result.decode("utf-8") if result else None

    
    
    # метод для удаления записи по ключу
    @classmethod
    async def delete(cls, key: str):
        redis_client = await get_redis_connection()
        
        result = await redis_client.execute_command("DEL", key)
        return "Данные удалены"
    
    
    # для проверки наличия users в базе и его создание 
    @classmethod
    async def check_and_create_redis_variable(cls, key: str, default_value: int):
        redis_client = await get_redis_connection()
        
        try:
            value = await redis_client.execute_command("GET", key)
            if value is None:
                await redis_client.execute_command("SET", key, default_value)
                return int(default_value)
            else:
                await redis_client.execute_command("SET", key, int(value)+1)
                return int(value)+1
            
        except:
            raise RedisConnectionError




