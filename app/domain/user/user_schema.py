from pydantic import Field
from utils import ObjectIdStr, MongoBaseModel

class User(MongoBaseModel):
    idx: int
    username: str
    password: str
