# HOLDS THE MODELS FOR THE TABLES

# imports

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# classes

class Post(Base):
    __tablename__ = 'posts'

    # columns
    id = Column(Integer, primary_key= True, nullable= False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable= False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default= 'TRUE', nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('NOW()'))
    user = relationship('User')  # we here are referencing the User class

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable= False, unique= True)  # unique will prevent the same email to be stored twice
    password = Column(String, nullable= True)
    created_at = Column(TIMESTAMP(timezone= True), nullable= False, server_default= text('NOW()'))

class Votes(Base):
    __tablename__ = 'votes'

    post_id = Column(
        Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key= True, nullable= False
        )
    user_id = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key= True, nullable= False
        )
