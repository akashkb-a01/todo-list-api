import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from model import Todo, User
from db import signup, signin

from passlib.context import CryptContext
from datetime import timedelta,datetime
from decouple import config
from jose import jwt

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

app = FastAPI()


# Routes
@app.get("/")
def get_index():
    return "We are live!!"

@app.post("/api/register")
async def register(user: User):
    user.password = CryptContext(schemes=["bcrypt"]).hash(user.password)
    response = await signup(user=user.dict())

    if response:
        return "User successfully registered!!"
    
    raise HTTPException(status_code=400, detail="Oops! Something went wrong. Try again.")

@app.post("/api/login")
async def login(user: OAuth2PasswordRequestForm=Depends()):
    response = await signin(username=user.username)
    if response:
        if CryptContext(schemes=["bcrypt"]).verify(user.password,response[1]):
            token = {
                "user":user.username,
                "exp":datetime.utcnow()+timedelta(hours=1)
                }
            token = jwt.encode(token,SECRET_KEY,ALGORITHM)
            return {"token":token}
    else:
        raise HTTPException(status_code=400, detail="Incorrect credentials.")