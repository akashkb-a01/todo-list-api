from pydantic import BaseModel, EmailStr

class Todo(BaseModel):
    title: str
    content: str

class User(BaseModel):
    username: str 
    email: EmailStr
    password: str
