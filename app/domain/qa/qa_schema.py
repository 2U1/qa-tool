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

class Quality(MongoBaseModel):
    quality: bool