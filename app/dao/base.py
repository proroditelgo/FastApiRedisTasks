from app.database import get_redis_connection





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