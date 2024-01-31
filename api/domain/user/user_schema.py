from pydantic import Field, field_validator
from utils import ObjectIdStr, MongoBaseModel
from pydantic_core.core_schema import FieldValidationInfo

class UserCreate(MongoBaseModel):
    idx: int
    username: str
    password1: str
    password2: str

    @field_validator('username', 'password1', 'password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('must not be empty')
        return v
    
    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('passwords do not match')
        return v
    
class Token(MongoBaseModel):
    access_token: str
    token_type: str
    username: str
