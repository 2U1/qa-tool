from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from domain.user import user_crud, user_schema
from database import get_user_db

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def user_create(_user_create: user_schema.UserCreate, db: AsyncIOMotorClient = Depends(get_user_db)):
    user = user_crud.get_exist_user(db, _user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    await user_crud.create_user(db, _user_create)