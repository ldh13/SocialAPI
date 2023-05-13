from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from . import oauth2
from .. import schemas, database, models

router = APIRouter(
    prefix='/votes',
    tags= ['vote']
)

@router.post('/', status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {vote.post_id} does not exist.'
        )
    vote_query = db.query(models.Votes).filter(
            models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)  # passing two conditions filters using both conditions
    vote_found = vote_query.first()
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail=f'User {current_user.id} has already voted on post with id {vote.post_id}'
                )
        new_vote = models.Votes(post_id= vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message':'Successfully added vote.'}
    else:
        if not vote_found:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail='Vote does not exist.'
                )
        vote_query.delete(synchronize_session= False)
        db.commit()

        return {'message':'Successfully deleted vote.'}
        

