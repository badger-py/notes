from typing import List

from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session

from dependices import get_db
from schemas import UserSchema, UserInSchema, UserUpdateSchema, UserSchema
from services.users import get_user, create_user, delete_user, update_user

users_enpoint = APIRouter(
    prefix="/api/users"
)

@users_enpoint.get('/get/{id}')
async def get_user_router(id: int, db: Session = Depends(get_db)) -> List[UserSchema]:
    return await get_user(id, db)


@users_enpoint.put('/create')
async def create_user_router(user: UserInSchema, db: Session = Depends(get_db)) -> UserSchema:
    try:
        return await create_user(user, db)
    except sqlalchemy.exc.IntegrityError as exc:
        raise HTTPException(400)

@users_enpoint.delete('/delete/{id}')
def delete_user_router(id: int, db: Session = Depends(get_db)):
    try:
        delete_user(id=id, db=db)
    except IndexError:
        raise HTTPException(404, "Note not found")
    
    return {"ok":True}

@users_enpoint.put('/update/{id}')
def update_user_router(id: int, user_to_update: UserUpdateSchema, db: Session = Depends(get_db)):
    try:
        update_user(id=id, user=user_to_update, db=db)
    except IndexError:
        raise HTTPException(404, "Note not found")
    
    return {"ok":True}
