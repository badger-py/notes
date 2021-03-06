from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserInSchema(BaseModel):
    name: str


class UserSchema(UserInSchema):
    """User out schema"""
    id: int

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: str


class NoteInSchema(BaseModel):
    title: str = "New note"
    text: str


class NoteSchema(NoteInSchema):
    """Note out model"""
    id: int
    published_at: datetime
    owner: UserSchema

    class Config:
        orm_mode = True


class NoteUpdateSchema(BaseModel):
    title: Optional[str]
    text: Optional[str]
