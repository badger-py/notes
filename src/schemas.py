from datetime import datetime
from typing import List
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    last_been_online: datetime

    class Config:
        orm_mode = True


class NoteSchema(BaseModel):
    id: int
    title: str = "New note"
    text: str
    owner_id: int

    owner: UserSchema

    class Config:
        orm_mode = True
