from pydantic import Field
from datetime import datetime
from utils import ObjectIdStr, MongoBaseModel

class VLMDataset(MongoBaseModel):
    idx: int
    image: str
    human: str
    gpt: str
    quality: bool
    date: str
    check: bool