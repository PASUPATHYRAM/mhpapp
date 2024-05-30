from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#creating sql engine

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:secret@localhost/MHP"

engine=create_engine(SQLALCHEMY_DATABASE_URL)

session=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()

