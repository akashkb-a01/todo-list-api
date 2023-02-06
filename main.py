from fastapi import FastAPI
from fastapi.security import oauth2
from model import Todo, User

app = FastAPI()