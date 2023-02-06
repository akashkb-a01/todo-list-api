from fastapi import FastAPI, HTTPException
from fastapi.security import oauth2
from model import Todo, User
from db import signup, login

from passlib.context import CryptContext

app = FastAPI()


# Routes
@app.get("/")
def get_index():
    return "We are live!!"

@app.post("/api/register")
async def register(user: User):
    user.password = CryptContext(schemes=["bcrypt"]).hash(user.password)
    response = await signup(user.dict())

    if response:
        return "User successfully registered!!"
    
    raise HTTPException(400, "Oops! Something went wrong. Try again.")