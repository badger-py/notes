from db import Base, SessionLocal, engine
from models import User, Note

from config import users, crate_test_notes

# create tables
# Base.metadata.create_all(bind=engine)

with SessionLocal() as db:

    created_users = []

    # create users from config
    for user_name in users:
        user = User(name=user_name, last_been_online=None)
        db.add(user)
        db.commit()
        db.refresh(user)
        created_users.append(user)

    if crate_test_notes:
        note = Note(
            text = "First note generated by create_db.py script",
            owner_id = created_users[0].id)
        db.add(note)
        db.commit()
        db.refresh(note)


print("db was creates sucesfully")