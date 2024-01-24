from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL

mongodb: AsyncIOMotorClient = None


async def connect_and_init_db():
    global mongodb
    
    try:
        mongodb = AsyncIOMotorClient(MONGODB_URL)

    except:
        raise Exception("Cannot connect to MongoDB")
    
async def close_db_connection():
    global mongodb

    if mongodb is None:
        return

    mongodb.close()
    mongodb = None

async def get_dataset_db():

    database = mongodb["dataset"]
    return database

async def get_user_db():

    database = mongodb['user']
    return database
