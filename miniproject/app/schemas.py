from pydantic import BaseModel

class Base(BaseModel):
    pass

class PostCreate(Base):
    title: str
    content: str

class PostResponse(Base):
    title: str
    content: str