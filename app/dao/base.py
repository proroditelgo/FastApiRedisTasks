from app.database import redis_client




class BaseDAO:
    model = None
    
    
    # метод для получения данных по айди
    @classmethod
    async def find_one_by_id(cls, model_id: int):
        result = await redis_client.get(f"model_{model_id}")
        return result.decode("utf-8") if result else None


    # метод для добавления данных в бд
    @classmethod
    async def add(cls, id, **data):
        result = await redis_client.set(id, **data)
        return "Данные добавлены"