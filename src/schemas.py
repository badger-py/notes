from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserInSchema(BaseModel):
    name: str


class UserSchema(UserInSchema):
    """User out schema"""
    id: int
    last_been_online: datetime

    class Config:
        orm_mode = True

class UserUpdateSchema(BaseModel):
    name: str


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
