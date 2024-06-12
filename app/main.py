from fastapi import FastAPI

from . import models
from . import database

from .router import post, user, auth

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
