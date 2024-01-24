from motor.motor_asyncio import AsyncIOMotorClient

async def get_vlm_dataset_list(db: AsyncIOMotorClient):
    cursor = db['vlm'].find({})

    dataset_list = [document async for document in cursor]

    return dataset_list