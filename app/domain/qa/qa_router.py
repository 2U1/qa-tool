from fastapi import APIRouter, Depends
from database import get_dataset_db
from domain.qa import qa_schema, qa_crud
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status 

router = APIRouter(
    prefix="/api/dataset",
)

@router.get("/vlm/list", response_model=list[qa_schema.VLMDataset])
async def vlm_dataset_list(db: AsyncIOMotorClient = Depends(get_dataset_db)):
    _dataset_list = await qa_crud.get_vlm_dataset_list(db)

    return _dataset_list

@router.get("/vlm/{data_idx}", response_model=qa_schema.VLMDataset)
async def vlm_single_data(data_idx: int, db: AsyncIOMotorClient = Depends(get_dataset_db)):
    _data = await qa_crud.get_vlm_data(db, data_idx=data_idx)

    return _data


@router.put("/vlm/quality/{data_idx}", status_code=status.HTTP_204_NO_CONTENT)
async def vlm_update_data(data_idx: int, quality: qa_schema.Quality, db: AsyncIOMotorClient = Depends(get_dataset_db)):
    await qa_crud.update_vlm_data(db, data_idx=data_idx, quality_check= quality)