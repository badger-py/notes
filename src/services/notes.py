from typing import List
from sqlalchemy.orm import Session

import models
import schemas


async def get_all_notes(db: Session, offset: int = 0, limit: int = 15) -> List[schemas.NoteSchema]:
    """Get notes

    Args:
        db (Session): db connction
        offset (int, optional) Defaults to 0.
        limit (int, optional) Defaults to 15.

    Returns:
        List[schemas.NoteSchema]: list of notes
    """
    return [i.to_model() for i in db.query(models.Note).offset(offset).limit(limit).all()]


async def create_note(note: schemas.NoteInSchema, db: Session) -> schemas.NoteSchema:
    """Create new note

    Args:
        note (schemas.NoteInSchema): note as pydantic schema
        db (Session): db connection

    Returns:
        schemas.NoteSchema: created note
    """
    new_note = models.Note(
        title=note.title,
        text=note.text,
        owner_id=note.owner_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return schemas.NoteSchema.from_orm(new_note)


def delete_note(id: int, db: Session) -> None:
    """Delete note by id

    Args:
        id (int): id of note
        db (Session): connection to db

    Raises:
        IndexError: if note not found
    """
    note_to_delete = db.query(models.Note).filter_by(id=id).first()

    if note_to_delete is None:
        raise IndexError('Note not found')

    db.delete(note_to_delete)
    db.commit()


def update_note(id: int, note: schemas.NoteUpdateSchema, db: Session) -> schemas.NoteSchema:
    note_to_update = db.query(models.Note).filter_by(id=id).first()

    if note_to_update is None:
        raise IndexError('Note not found')

    data = note.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(note_to_update, key, value)

    db.add(note_to_update)
    db.commit()
    db.refresh(note_to_update)
    return schemas.NoteSchema.from_orm(note_to_update)
