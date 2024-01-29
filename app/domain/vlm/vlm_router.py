from fastapi import APIRouter, Depends
from domain.vlm import vlm_crud, vlm_schema
from database import get_dataset_db
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status 

router = APIRouter(
    prefix="/api/dataset",
)

@router.get("/vlm/list", response_model=vlm_schema.VLMDatasetList)
async def vlm_dataset_list(db: AsyncIOMotorClient = Depends(get_dataset_db), page: int = 0, size: int=10):
    offset = (page-1)*size if page > 0 else 0
    total, _dataset_list = await vlm_crud.get_vlm_dataset_list(db, skip=offset, limit=size)

    return {'total': total, 'dataset_list': _dataset_list}

@router.get("/vlm/detail/{data_idx}", response_model=vlm_schema.VLMDataset)
async def vlm_single_data(data_idx: int, db: AsyncIOMotorClient = Depends(get_dataset_db)):
    _data = await vlm_crud.get_vlm_data(db, data_idx=data_idx)

    return _data

@router.get("/vlm/info/idx", response_model=vlm_schema.VLMIdx)
async def vlm_get_idx(db: AsyncIOMotorClient = Depends(get_dataset_db)):
    first_idx, last_idx = await vlm_crud.get_first_last_idx(db)

    return {'first_idx': first_idx, 'last_idx': last_idx}


@router.put("/vlm/quality/{data_idx}", status_code=status.HTTP_204_NO_CONTENT)
async def vlm_update_data(data_idx: int, quality: vlm_schema.Quality, db: AsyncIOMotorClient = Depends(get_dataset_db)):
    await vlm_crud.update_vlm_data(db, data_idx=data_idx, quality_check= quality)