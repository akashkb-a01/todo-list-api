import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from model import Todo, User
from db import signup, signin, fetch_user_todos, create_todo, fetch_all_todos, fetch_one_todo, update_todo, remove_todo

from passlib.context import CryptContext
from datetime import timedelta,datetime
from decouple import config
import jwt
import uuid

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return username


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

@app.post("/token")
async def login(user: OAuth2PasswordRequestForm=Depends()):
    response = await signin(username=user.username)
    if response:
        if CryptContext(schemes=["bcrypt"]).verify(user.password,response[1]):
            token = {
                "sub":user.username,
                "exp":datetime.utcnow()+timedelta(hours=1)
                }
            token = jwt.encode(token,SECRET_KEY,ALGORITHM)
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400, detail="Incorrect password.")
            
    else:
        raise HTTPException(status_code=400, detail="Invalid username.")

@app.get("/api/todos")
async def user_todos(username: User = Depends(get_current_user)):
    return await fetch_user_todos(username)

@app.post("/api/create")
async def new_todo(title: str, content: str, username: str = Depends(get_current_user)):
    todo: Todo
    todo.title = title
    todo.content = content
    todo.username = username
    todo.id = str(uuid.uuid1())
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(status_code=400,detail="Could not create TODo")

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo{title}", dependencies=[Depends(oauth2_scheme)] ,response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no Todo item with this title {title}")


@app.post("/api/todo", dependencies=[Depends(oauth2_scheme)] ,response_model=Todo)
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")


@app.put("/api/todo{title}/",dependencies=[Depends(oauth2_scheme)],response_model=Todo)
async def put_todo(title:str,cont:str):
    response = await update_todo(title, cont)
    if response:
        return response
    raise HTTPException(404, f"There is no Todo item with this title {title}")


@app.delete("/api/todo{title}",dependencies=[Depends(oauth2_scheme)])
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo item"
    raise HTTPException(404, f"There is no Todo item with this title {title}")