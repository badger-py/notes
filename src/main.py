from email import header
from fastapi import FastAPI, Header

from notes_endpoints import notes_endpoint
from users_enpoints import users_enpoint


app = FastAPI(title="Notes app API")


app.include_router(notes_endpoint)
app.include_router(users_enpoint)

@app.get('/test')
def test():
    return str(Header("Authorization"))