from typing import List

from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session

from dependices import get_db
from schemas import NoteSchema, NoteInSchema, NoteUpdateSchema, UserSchema
from services.notes import get_all_notes, create_note, delete_note, update_note

notes_endpoint = APIRouter(
    prefix="/api/notes"
)


@notes_endpoint.get('/', response_model=List[NoteSchema],tags=["notes"])
async def get_all_notes_router(db: Session = Depends(get_db), offset: int = 0, limit: int = 15) -> List[NoteSchema]:
    return await get_all_notes(db, offset=offset, limit=limit)

@notes_endpoint.post('/', response_model=NoteSchema, tags=["notes"])
async def create_note_router(note: NoteInSchema, db: Session = Depends(get_db)) -> NoteSchema:
    try:
        return await create_note(note, db)
    except sqlalchemy.exc.IntegrityError as exc:
        raise HTTPException(400)

@notes_endpoint.delete('/{id}', tags=["notes"])
def delete_note_router(id: int, db: Session = Depends(get_db)):
    try:
        delete_note(id=id, db=db)
    except IndexError:
        raise HTTPException(404, "Note not found")
    
    return {"ok":True}

@notes_endpoint.put('/{id}', response_model=NoteSchema, tags=["notes"])
def update_note_router(id: int, note_to_update: NoteUpdateSchema, db: Session = Depends(get_db)):
    try:
        updated_note = update_note(id=id, note=note_to_update, db=db)
    except IndexError:
        raise HTTPException(404, "Note not found")
    
    return updated_note
