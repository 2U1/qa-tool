from pydantic import Field
from utils import MongoBaseModel

class Conversation(MongoBaseModel):
    index: int
    speaker: str
    value: str
    quality: bool

class VLMDataset(MongoBaseModel):
    idx: int 
    image: str 
    conversations: list[Conversation]
    date: str 
    check: bool

class VLMDatasetList(MongoBaseModel):
    total: int
    dataset_list: list[VLMDataset]

class Quality(MongoBaseModel):
    index: int
    quality: bool

class VLMIdx(MongoBaseModel):
    first_idx: int
    last_idx: int

class VLMDatasetProgress(MongoBaseModel):
    total: int
    progress: int