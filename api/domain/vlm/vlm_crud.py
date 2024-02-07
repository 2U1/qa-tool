from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from domain.vlm.vlm_schema import Quality
from pytz import timezone
import json

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
    await db['vlm'].update_one({'idx':data_idx, "conversations.index": quality_check.index}, {'$set': {'conversations.$.quality':quality_check.quality,'date':datetime.now(timezone('Asia/Seoul')).isoformat(),'check': True}})


async def insert_vlm_data(db: AsyncIOMotorClient, data):

    existing_images = {doc['image'] async for doc in db['vlm'].find({}, {'image': 1})}
    
    data_list = []

    last_idx = await db['vlm'].count_documents({})

    count = 0
    
    for d in data:
        if d['image'] in existing_images:
            continue
        index = last_idx + count
        image = d['image']
        conversation = d['conversations']
        conversation = [{'index':i,'speaker':c['from'], 'value':c['value'], 'quality':False} for i, c in enumerate(conversation)]
        date = datetime.now(timezone('Asia/Seoul')).isoformat()
        check = False

        data_list.append({'idx':index, 'image':image, 'conversations': conversation, 'date':date, 'check':check})

        if len(data_list) == 100:
            await db['vlm'].insert_many(data_list)
            data_list = []

        count += 1
    
    if data_list:
        await db['vlm'].insert_many(data_list)


async def download_vlm_data(db: AsyncIOMotorClient, file_path: str):
    cursor = db['vlm'].find({}, {'_id':0, 'date':0, 'check':0}).sort("idx", 1)
    data = [document async for document in cursor]

    with open(file_path + 'vlm.json', 'w') as f:
        json.dump(data, f, indent=4)

    return file_path + 'vlm.json'