# imports 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, vote, auth
from .config import settings

# instantiating models

# models.Base.metadata.create_all(bind= engine) # alembic is now running the migrations

# initializing app

app = FastAPI()

# allowing other servers to access the api

origins = [
    '*'  # all domains can access the api server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods= ['*'],
    allow_headers= ['*']
)

# routes

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')      # stablish the home route
def root():
    return {'message':'Welcome to my API!'}  # the python dictionary will be converted to JSON

