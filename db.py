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