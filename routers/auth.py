from fastapi import APIRouter
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
import models
from user_request import UserRequest
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/auth/createuser/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    create_user_model = models.User(
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "User created successfully", "user": create_user_model}

@router.get("/auth/users/", status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
    return db.query(models.User).all()

@router.delete("/auth/deleteuser/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: int):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is not None:
        db.delete(user_model)
        db.commit()
        return {"message": f"User with id {user_id} deleted successfully"}
    return {"message": f"User with id {user_id} not found"}