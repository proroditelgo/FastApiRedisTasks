from fastapi import APIRouter, Depends, Response


from app.exceptions import CustomExceptions, UserAlreadyExistsException

from app.users.dependencies import get_current_user
from app.users.schema import SUser
from app.users.dao import UserDAO

from app.users.auth import authenticate_user, create_access_token, get_password_hash







router = APIRouter(
    prefix="/auth",
    tags=["Регистрация и пользователи"]
)






@router.post("/register")
async def register_user(user_data: SUser):
    
    existing_user = await UserDAO.find_user(email=user_data.email)
    
    if existing_user:
        raise CustomExceptions
    
    hashed_password = get_password_hash(user_data.password)
    
    await UserDAO.add_user(email=user_data.email, hashed_password=str(hashed_password))
    
    
    
    
    
@router.post("/login")
async def login_user(response: Response, user_data: SUser):
    user = await authenticate_user(user_data.email, user_data.password)
    
    if not user:
        raise UserAlreadyExistsException
    
    
    acces_token = create_access_token({"sub": str(user[0])})
    response.set_cookie("user_access_token", acces_token, httponly=True)
    
    return acces_token



@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")
    
    
    
@router.get("/me")
async def read_user_me(current_user: list = Depends(get_current_user)):
    return current_user