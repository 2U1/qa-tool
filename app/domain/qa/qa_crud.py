from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from domain.qa.qa_schema import Quality

async def get_vlm_dataset_list(db: AsyncIOMotorClient):
    cursor = db['vlm'].find({})

    dataset_list = [document async for document in cursor]

    return dataset_list

async def get_vlm_data(db: AsyncIOMotorClient, data_idx: int):
    cursor = db['vlm'].find_one({'idx':data_idx})

    return await cursor

async def update_vlm_data(db: AsyncIOMotorClient, data_idx: int, quality_check: Quality):
    db['vlm'].update_one({'idx':data_idx}, {'$set': {'quality':quality_check.quality,'date':datetime.now().isoformat(),'check': True}})