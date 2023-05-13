# imports

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# variables

SQLALCHEMY_DATABASE_URL = \
f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush= False, bind= engine 
    )

# creating the base class

Base = declarative_base()

# dependencies

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# creating database connection

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='SocialAPI',
#                                 user='postgres', password='Samsara13samsara',
#                                 cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was succesful.')
#         break

#     except Exception as error:
#         print('Connecting to database failed.')
#         print(error)
#         time.sleep(2)  # we retry to connect every two seconds
