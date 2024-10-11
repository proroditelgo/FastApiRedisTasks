from fastapi import HTTPException, status




class CustomExceptions(HTTPException):
    
    status_code = 500
    
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)




# пользователя не существует
class UserIsNotPresent(CustomExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED



class TokenExpireException(CustomExceptions):
    
    status_code = status.HTTP_401_UNAUTHORIZED
    detail="Время токена истекло"


class TokenException(CustomExceptions):
    
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Проблема с токеном"
    

class UserAlreadyExistsException(CustomExceptions):
    
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь не найден"
    
    
    
class AvailableTokenException(CustomExceptions):
    
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Нет токена"
    

class TaskIsNotPresent(CustomExceptions):
    
    status_code=status.HTTP_404_NOT_FOUND
    detail="Такой задачи не существует"