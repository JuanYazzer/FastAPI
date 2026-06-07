from pydantic import BaseModel
from fastapi_users import schemas
import uuid

class Base(BaseModel):
    pass

class PostCreate(Base):
    title: str
    content: str

class PostResponse(Base):
    title: str
    content: str

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass