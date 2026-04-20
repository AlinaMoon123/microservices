from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    accept_password: str

class User():
    user_id: int
    name: str
    email: EmailStr
    role: str

class Login(BaseModel):
    email: str
    password: str
    


