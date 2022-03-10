from typing import List

from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session

from dependices import get_db
from schemas import UserSchema, UserInSchema, UserUpdateSchema, UserSchema
from services.users import get_user, get_all_users, create_user, delete_user, update_user

users_enpoint = APIRouter(
    prefix="/api/users"
)

@users_enpoint.get('/')
async def get_all_users_router(db: Session = Depends(get_db)) -> List[UserSchema]:
    return get_all_users(db)

@users_enpoint.get('/{id}')
async def get_user_router(id: int, db: Session = Depends(get_db)) -> UserSchema:
    return await get_user(id, db)

@users_enpoint.post('/')
async def create_user_router(user: UserInSchema, db: Session = Depends(get_db)) -> UserSchema:
    try:
        return await create_user(user, db)
    except sqlalchemy.exc.IntegrityError as exc:
        raise HTTPException(400)

@users_enpoint.delete('/{id}')
def delete_user_router(id: int, db: Session = Depends(get_db)):
    try:
        delete_user(id=id, db=db)
    except IndexError:
        raise HTTPException(404, "Note not found")
    
    return {"ok":True}

@users_enpoint.put('/{id}')
def update_user_router(id: int, user_to_update: UserUpdateSchema, db: Session = Depends(get_db)):
    try:
        update_user(id=id, user=user_to_update, db=db)
    except IndexError:
        raise HTTPException(404, "Note not found")
    
    return {"ok":True}
