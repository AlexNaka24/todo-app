# IMPORTS
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from database import SessionLocal
import models
from routers.auth import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session

# Router for admin
router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# Creates a new session for each petition and then it closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for database session      
db_dependency = Annotated[Session, Depends(get_db)]

# Dependency for current user from token
user_dependency = Annotated[dict, Depends(get_current_user)]

# GET all todos (only for admin)
@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource, you are not an admin")
    return db.query(models.Todos).all()

# GET all users
@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource, you are not an admin")
    return db.query(models.User).all()

# GET user by id
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user_by_id(db: db_dependency, user: user_dependency, user_id: int):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource, you are not an admin")
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} was not found")
    return f"User with id {user_id} was found", f"User: {user_model}"