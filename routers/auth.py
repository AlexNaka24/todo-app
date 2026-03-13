
from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def get_user():
    return {"message": "Login endpoint"}
