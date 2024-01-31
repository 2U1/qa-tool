from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from domain.vlm.vlm_schema import Quality
from pytz import timezone

async def get_first_last_idx(db: AsyncIOMotorClient):
    cursor = db['vlm'].find({}).sort("idx", 1).limit(1)
    first_idx = [document async for document in cursor]
    cursor = db['vlm'].find({}).sort("idx", -1).limit(1)
    last_idx = [document async for document in cursor]
    
    return first_idx[0]['idx'], last_idx[0]['idx']

async def get_vlm_dataset_list(db: AsyncIOMotorClient, skip: int = 0, limit: int = 10, check: str = 'all'):
    cursor = db['vlm']

    query = {}

    if check != 'all':
        query['check'] = True if check == 'true' else False

    total = await cursor.count_documents({})
    docs = cursor.find(query).sort("idx", 1).limit(limit).skip(skip)

    dataset_list = [document async for document in docs]

    return total, dataset_list

async def get_vlm_data(db: AsyncIOMotorClient, data_idx: int):
    cursor = db['vlm'].find_one({'idx':data_idx})

    return await cursor

async def update_vlm_data(db: AsyncIOMotorClient, data_idx: int, quality_check: Quality):
    db['vlm'].update_one({'idx':data_idx}, {'$set': {'quality':quality_check.quality,'date':datetime.now(timezone('Asia/Seoul')).isoformat(),'check': True}})