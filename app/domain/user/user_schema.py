from pydantic import Field
from utils import ObjectIdStr, MongoBaseModel

class User(MongoBaseModel):
    id: ObjectIdStr = Field(alias="_id")
    username: str
    password: str
