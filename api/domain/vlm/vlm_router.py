from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from domain.vlm import vlm_crud, vlm_schema
from database import get_dataset_db
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
import os
import mimetypes
import orjson

router = APIRouter(
    prefix="/api/dataset",
)

@router.get("/vlm/list", response_model=vlm_schema.VLMDatasetList)
async def vlm_dataset_list(db: AsyncIOMotorClient = Depends(get_dataset_db), page: int = 0, size: int=10, check: str = 'all'):
    offset = (page-1)*size if page > 0 else 0
    total, _dataset_list = await vlm_crud.get_vlm_dataset_list(db, skip=offset, limit=size, check=check)

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

@router.get("/vlm/list/progress", response_model=vlm_schema.VLMDatasetProgress)
async def vlm_dataset_progress(db: AsyncIOMotorClient = Depends(get_dataset_db)):
    total, _dataset_list = await vlm_crud.get_vlm_dataset_list(db, skip=0, limit=0, check='true')
    progress = len(_dataset_list)

    return {'total': total, 'progress': progress}

@router.get("/vlm/image/{file_name}")
async def vlm_get_image(file_name: str):
    image_path = "/home/workspace/data/vlm/images/train2017/" + file_name
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    mime_type, _ = mimetypes.guess_type(image_path)

    return FileResponse(image_path, media_type=mime_type or "application/octet-stream")

@router.post("/vlm/upload", status_code=status.HTTP_204_NO_CONTENT)
async def vlm_upload_data(file: UploadFile = File(...), db: AsyncIOMotorClient = Depends(get_dataset_db)):
    file_contents = await file.read()

    data = orjson.loads(file_contents)

    await vlm_crud.insert_vlm_data(db, data)



@router.get("/vlm/download")
async def vlm_download_data(db: AsyncIOMotorClient = Depends(get_dataset_db)):
    file_path = "/home/workspace/data/vlm/exported/"
    
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    await vlm_crud.download_vlm_data(db, file_path)