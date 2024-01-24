from fastapi import APIRouter, Depends
from database import get_dataset_db
from domain.qa import qa_schema, qa_crud
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(
    prefix="/api/dataset",
)

@router.get("/vlm/list", response_model=list[qa_schema.VLMDataset])
async def vlm_dataset_list(db: AsyncIOMotorClient = Depends(get_dataset_db)):
    _dataset_list = await qa_crud.get_vlm_dataset_list(db)

    return _dataset_list