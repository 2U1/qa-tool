from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from domain.user import user_crud, user_schema
from database import get_user_db
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from domain.user.user_crud import pwd_context
from starlette.config import Config

config = Config(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
SECRET_KEY = config("SECRET_KEY", cast=str)
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def user_create(_user_create: user_schema.UserCreate, db: AsyncIOMotorClient = Depends(get_user_db)):
    user = await user_crud.get_exist_user(db, _user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    await user_crud.create_user(db, _user_create)

@router.post("/login", response_model=user_schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_user_db)):
    user = await user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    data = {
        "sub": user['username'],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer", "username": user['username']}