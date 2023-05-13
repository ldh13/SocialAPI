# imports

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import oauth2
from .. import database, schemas, models, utils

# instantiating router

router = APIRouter(
    prefix='/login',
    tags= ['Authentication']
)

# login route

@router.post('/', response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()  # we use username because is the format of the OAuth2PasswordRequestForm
    if not user:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN, detail='Invalid credentials.')
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN, detail='Invalid credentials.')
    # create a token and return it to the user
    access_token = oauth2.create_access_token(data= {'user_id':user.id})
    return {'access_token':access_token, 'token_type':'bearer'}
