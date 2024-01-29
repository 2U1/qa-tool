from pydantic import Field
from utils import MongoBaseModel

class VLMDataset(MongoBaseModel):
    idx: int 
    image: str 
    human: str 
    gpt: str 
    quality: bool
    date: str 
    check: bool

class VLMDatasetList(MongoBaseModel):
    total: int
    dataset_list: list[VLMDataset]

class Quality(MongoBaseModel):
    quality: bool

class VLMIdx(MongoBaseModel):
    first_idx: int
    last_idx: int