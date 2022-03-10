from typing import List
from sqlalchemy.orm import Session

import models
import schemas


def get_all_users(db: Session) -> List[schemas.UserSchema]:
    """Get all users

    Args:
        db (Session): connection to db

    Returns:
        List[schemas.UserSchema]: list of users
    """
    users = db.query(models.User).all()
    return [schemas.UserSchema.from_orm(user) for user in users]


async def get_user(id: int, db: Session) -> schemas.UserSchema:
    """Get user by id

    Args:
        db (Session): connection to db
        id (int): if of user

    Returns:
        schemas.UserSchema: user as pydatic model
    """
    return db.query(models.User).filter_by(id=id).first()


async def create_user(user: schemas.UserInSchema, db: Session) -> schemas.UserSchema:
    """Create user

    Args:
        user (schemas.UserInSchema): user's data
        db (Session): connection to db

    Returns:
        schemas.UserSchema: created user
    """
    new_user = models.User(
        name=user.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schemas.UserSchema.from_orm(new_user)


def delete_user(id: int, db: Session) -> None:
    """Delete user by id

    Args:
        id (int): id of user
        db (Session): connection to db

    Raises:
        IndexError: if user not found
    """
    user_to_delete = db.query(models.User).filter_by(id=id).first()

    if user_to_delete is None:
        raise IndexError('User not found')

    db.delete(user_to_delete)
    db.commit()


def update_user(id: int, user: schemas.UserUpdateSchema, db: Session) -> schemas.UserSchema:
    """Update user by id

    Args:
        id (int): id of user
        user (schemas.UserUpdateSchema): new user data
        db (Session): connection to db

    Raises:
        IndexError: if user not found

    Returns:
        schemas.UserSchema: _description_
    """
    user_to_update = db.query(models.User).filter_by(id=id).first()

    if user_to_update is None:
        raise IndexError('Note not found')

    data = user.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(user_to_update, key, value)

    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)
    return schemas.UserSchema.from_orm(user_to_update)
