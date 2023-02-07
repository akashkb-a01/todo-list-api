from model import Todo, User
# DB of choice - MongoDB
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.Todo
todos = db.todo
users = db.user

async def signin(username):
    user = await users.find_one({"username":username})

    if user:
        password = user["password"]
        return [username,password]

    return False

async def signup(user):
    return await users.insert_one(user)

async def fetch_one_todo(title):
    document = await todos.find_one({"title":title})
    return document

async def fetch_all_todos():
    todol = []
    cursor = todos.find({})
    async for document in cursor:
        todol.append(Todo(**document))
    return todol

async def fetch_user_todos(username):
    todol = []
    cursor = todos.find({"username":username})
    async for document in cursor:
        todol.append(Todo(**document))
    return todol

async def create_todo(todo):
    return await todos.insert_one(todo)

async def update_todo(title, desc):
    return await todos.update_one({"title":title},{"$set":{"description":desc}})

async def remove_todo(title):
    await todos.delete_one({"title":title})
    return True