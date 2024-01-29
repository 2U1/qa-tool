from motor.motor_asyncio import AsyncIOMotorClient
from domain.user.user_schema import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: AsyncIOMotorClient, user_create: UserCreate):
    db['user'].insert_one({'idx':user_create.idx, 
                           'username':user_create.username, 
                           'password':pwd_context.hash(user_create.password1)})
    
def get_exist_user(db: AsyncIOMotorClient, user_create: UserCreate):
    cursor = db['user'].find_one({'username':user_create.username})
    
    return cursor