import bcrypt
from datetime import datetime, timedelta, timezone

from jose import jwt
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UserDAO


key=settings.KEY
algorithm=settings.ALGORITHM






# создание хеша пароля
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())




# сравнение хешей пароля
def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password)




# создание токена
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp":expire})
    
    encoded_jwt = jwt.encode(
        to_encode, key, algorithm
    )
    
    return encoded_jwt




# проверка пользователя при логине
async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_user(email=email)
    
    
    if not user and not verify_password(password, user[1]):
        return None

    return user