# imports

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from . import oauth2
from .. import models, schemas, utils
from ..database import get_db

# initializing router

router = APIRouter(
    prefix='/posts',
    tags= ['Posts']
)

# routes
# , response_model= List[schemas.PostResponse]
@router.get('/', response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ''):  # set the limit number of posts to 10 by default
    # QUERY = 'SELECT * FROM POSTS'
    # cursor.execute(QUERY)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search) | models.Post.content.contains(search)).limit(limit).offset(skip).all()
    posts = (
        db.query(models.Post, func.count(models.Votes.post_id).label('votes'))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter= True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search) | models.Post.content.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
        )  # this is a left outer join
    
    return posts # it will be automatically serialized into JSON

# for posts we want a title as a string and content as a string
@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):  # this will extract all the info in the body and load it as a python dict
    # QUERY = 'INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;'
    # cursor.execute(QUERY, (post.title, post.content, post.published))  # passing the values in the second field will prevent SQL injections
    # new_post = cursor.fetchone()                                       # we now get what is returned from the query
    # conn.commit()                                                      # pushing changes out
    new_post = models.Post(user_id= current_user.id, **post.dict())  # unpacks all fields present in the model
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get('/{id}', response_model= schemas.PostResponse)  # this id  field is called a path parameter, they are always passed as strings
def get_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):   # this will validate that id can be converted to an int and will convert it for us
    # QUERY = 'SELECT * FROM posts WHERE id = %s'
    # cursor.execute(QUERY, (id,))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = (
        db.query(models.Post, func.count(models.Votes.post_id).label('votes'))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter= True)
        .group_by(models.Post.id).filter(models.Post.id == id).first()
    )
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} was not found.')
    
    return post

# DELETING POSTS
@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # QUERY = 'DELETE FROM  posts WHERE id = %s RETURNING *;'
    # cursor.execute(QUERY, (id,))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:  # if the query returns nothing we raise a 404
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id {id} does not exist.')
    if post.first().user_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action.'
        )
    post.delete(synchronize_session= False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)

# UPDATING POSTS
@router.put('/{id}', response_model= schemas.PostResponse)  # put allows to change a post but requires to reintroduce all fields in the post
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # QUERY = 'UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING*;'
    # cursor.execute(QUERY, (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()
    if post_to_update is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id {id} does not exist.')
    if post_to_update.user_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action.'
        )
    post_query.update(post.dict(), synchronize_session= False)
    db.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    return updated_post
