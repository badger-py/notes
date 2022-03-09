from datetime import utcnow

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        relationship)
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    last_been_online = Column(DateTime, default=utcnow)
    
    notes = relationship('Note', bacref='owner')


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, default="New note")
    text = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", backref="notes")
