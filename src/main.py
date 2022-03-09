from fastapi import FastAPI

from .notes_endpoints import notes_endpoint

app = FastAPI()

app.include_router(notes_endpoint)