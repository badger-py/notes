from re import A
from typing import List

from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session

from dependices import get_db,  auth_header
from exceptions import AccessDenied
from schemas import NoteSchema, NoteInSchema, NoteUpdateSchema, UserSchema
from services.notes import get_all_notes, create_note, delete_note, update_note

notes_endpoint = APIRouter(
    prefix="/api/notes"
)


@notes_endpoint.get('/', response_model=List[NoteSchema],tags=["notes"])
async def get_all_notes_router(db: Session = Depends(get_db), offset: int = 0, limit: int = 15) -> List[NoteSchema]:
    return await get_all_notes(db, offset=offset, limit=limit)

@notes_endpoint.post('/', response_model=NoteSchema, tags=["notes"])
async def create_note_router(note: NoteInSchema, user_id: int = auth_header, db: Session = Depends(get_db)) -> NoteSchema:
    if user_id is None:
        raise HTTPException(401)
    
    try:
        return await create_note(note=note, user=user_id, db=db)
    except sqlalchemy.exc.IntegrityError as exc:
        raise HTTPException(400)

@notes_endpoint.delete('/{id}', tags=["notes"])
def delete_note_router(id: int, user_id: int = auth_header, db: Session = Depends(get_db)):
    try:
        delete_note(id=id, user_id=user_id, db=db)
    except IndexError:
        raise HTTPException(404, "Note not found")
    except AccessDenied:
        raise HTTPException(401) # Unath
    
    return {"ok":True}

@notes_endpoint.put('/{id}', response_model=NoteSchema, tags=["notes"])
def update_note_router(id: int, note_to_update: NoteUpdateSchema, user_id: int = auth_header, db: Session = Depends(get_db)):
    try:
        updated_note = update_note(id=id, note=note_to_update, user_id=user_id, db=db)
    except IndexError:
        raise HTTPException(404, "Note not found")
    except AccessDenied:
        raise HTTPException(401) # Unath
    
    return updated_note
