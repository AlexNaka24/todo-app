# IMPORTS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL of the database sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Engine / connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Fabric of sessions, gives a new session to use 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the base class from which all your models (tables) inherit in SQLAlchemy
Base = declarative_base()