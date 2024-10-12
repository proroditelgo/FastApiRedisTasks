from fastapi import HTTPException, status




class CustomExceptions(HTTPException):
    
    status_code = 500
    
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)



# ==========ОШИБКИ АВТОРИЗАЦИИ и РЕГИСТРАЦИИ===============
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
# ====================================================== 

    
# ================ОШИБКИ ВВОДА==========================
class ParamIsImmutable(CustomExceptions):
    
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Данный параметр нельзя изменить. Менять можно: title, description, due_data, is_completed, priority" 
    
    
class ParamIsNotDate(CustomExceptions):
    
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Параметр не является датой, формат ГГГГ-ММ-ДД" 
    
class ParamIsNotBool(CustomExceptions):
    
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Параметр не является bool, формат false или true" 
    
    
class InputError(CustomExceptions):
    
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Текст некорректный или обнаружен код" 
    
class LenError(CustomExceptions):
    
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Заголовок задачи должен быть менее 100 символов" 
    
class PriorityError(CustomExceptions):
    
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Неправильно указан приоритет, формат low, medium или high" 
    
# ====================================================== 
