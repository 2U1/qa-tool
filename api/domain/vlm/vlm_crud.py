from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from domain.vlm.vlm_schema import Quality
from pytz import timezone
import orjson

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
    db['vlm'].update_one({'idx':data_idx, "conversations.index": quality_check.index}, {'$set': {'conversations.$.quality':quality_check.quality,'date':datetime.now(timezone('Asia/Seoul')).isoformat(),'check': True}})


async def insert_vlm_data(db: AsyncIOMotorClient, file_name: str):
    data_path = '/home/workspace/data/vlm/text/' + file_name
    data_list = []
    
    with open(data_path, 'r') as f:
        data = orjson.load(f)

    try:
        _, last_idx = await get_first_last_idx(db)
    
    except:
        last_idx = 0
    
    for idx, d in enumerate(data):
        if db['vlm'].find_one({'image':d['image']}):
            continue
        index = last_idx + idx
        image = d['image']
        conversation = d['conversations']
        conversation = [{'index':i,'speaker':c['speaker'], 'value':c['value'], 'quality':False} for i, c in enumerate(conversation)]
        date = datetime.now(timezone('Asia/Seoul')).isoformat()
        check = False

        data_list.append({'idx':index, 'image':image, 'conversation': conversation, 'date':date, 'check':check})

    db['vlm'].insert_many(data_list)