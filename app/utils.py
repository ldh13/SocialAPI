# imports

from passlib.context import CryptContext

# variables

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')  # setting the hashing algorithm

# functions

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)