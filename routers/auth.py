from datetime import timedelta, datetime, timezone
from fastapi import APIRouter
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
import models
from schemas.user_request import UserRequest
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from schemas.token_squema import Token

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "234654gf8768fgf679867jgfsad1231254345sdfgds67532231dfghj67ui4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# POST users
@router.post("/createuser", status_code=status.HTTP_201_CREATED)
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

# POST token
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return {"message": "Incorrect username or password"}
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

# GET users
@router.get("/users", status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
    return db.query(models.User).all()

# DELETE users by userid
@router.delete("/deleteuser/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: int):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is not None:
        db.delete(user_model)
        db.commit()
        return {"message": f"User with id {user_id} deleted successfully"}
    return {"message": f"User with id {user_id} not found"}