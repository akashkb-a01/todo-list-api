from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str 
    email: EmailStr
    password: str

class Todo(BaseModel):
    username: str
    id: str
    title: str
    content: str
