from fastapi import Depends, FastAPI

from notes_endpoints import notes_endpoint
from users_enpoints import users_enpoint

from db import SessionLocal

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(notes_endpoint)
app.include_router(users_enpoint)