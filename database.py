# IMPORTS
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # Load environment variables from .env file

# URL of the database sqlite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Engine / connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fabric of sessions, gives a new session to use 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the base class from which all your models (tables) inherit in SQLAlchemy
Base = declarative_base()