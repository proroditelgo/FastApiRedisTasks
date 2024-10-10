from app.database import get_redis_connection




class BaseDAO:
    
    # метод для получения данных по почте
    @classmethod
    async def find_one(cls, key: str):
        redis_client = await get_redis_connection()

        result = await redis_client.execute_command("GET", key)
        return result.decode("utf-8") if result else None


    # метод для добавления данных в бд
    @classmethod
    async def add(cls, id, **data):
        redis_client = await get_redis_connection()

        result = await redis_client.execute_command("SET", id, **data)
        return "Данные добавлены"
    
    
