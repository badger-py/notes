from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserInSchema(BaseModel):
    name: str
    last_been_online: datetime


class UserSchema(UserInSchema):
    id: int

    class Config:
        orm_mode = True

class UserUpdateSchema(BaseModel):
    pass


class NoteInSchema(BaseModel):
    title: str = "New note"
    text: str
    owner_id: int


class NoteSchema(NoteInSchema):
    id: int
    owner: UserSchema

    class Config:
        orm_mode = True


class NoteUpdateSchema(BaseModel):
    title: Optional[str]
    text: Optional[str]
    owner_id: Optional[int]
