from pydantic import BaseModel, EmailStr





class SUser(BaseModel):
    
    email: EmailStr
    password: str
    
    
    class ConfigDict:
        from_attributes = True