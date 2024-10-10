from pydantic import BaseModel, EmailStr, Field





class SUser(BaseModel):
    
    email: EmailStr
    password: str
    
    
    class ConfigDict:
        from_attributes = True