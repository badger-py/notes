from fastapi import Header

from db import SessionLocal


# Dependencies:

# auth header
auth_header = Header(None, alias="Authorization")


def get_db():
    db = SessionLocal()
    try:
        # for sqlite3
        db.execute("PRAGMA foreign_keys = ON;")
        yield db
    finally:
        db.close()
