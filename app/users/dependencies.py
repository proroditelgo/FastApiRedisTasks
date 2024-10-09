from datetime import datetime, timezone
from fastapi import Request, Depends
from jose import jwt, JWTError
from pydantic import EmailStr


from app.users.dao import UserDAO
from app.exceptions import (AvailableTokenException, 
                            TokenException, 
                            TokenExpireException, 
                            UserIsNotPresent)
from app.config import settings



key=settings.KEY
algorithm=settings.ALGORITHM


# получение токена из куки
def get_token(request: Request):
    
    token = request.cookies.get("user_access_token")
    
    if not token:
        raise AvailableTokenException
    return token




async def get_current_user(token: str = Depends(get_token)):
    
    try:
        
        payload=jwt.decode(
            token, key, algorithm
        )
        
    
    except JWTError:
        raise TokenException
        
    # время действия токена
    expire: str = payload.get("exp")
    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpireException
    
    # наличие почты
    email: EmailStr = payload.get("sub")
    if not email:
        raise UserIsNotPresent
    
    # наличие пользователя в базе
    user = await UserDAO.find_user(str(email))
    if not user:
        raise UserIsNotPresent  
    
    
    return user