from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, TypeDecorator
from sqlalchemy.orm import relationship

from schemas import NoteSchema

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    last_been_online = Column(DateTime, default=datetime.utcnow)

    # notes: List[Note]


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, default="New note")
    text = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", backref="notes", foreign_keys=[owner_id])

    def to_model(self) -> NoteSchema:
        return NoteSchema.from_orm(self)
