from fastapi import APIRouter, Depends
from app.schemas import UserOut
from app import auth_utils

router = APIRouter()

@router.get("/me", response_model=UserOut)
def get_me(current_user=Depends(auth_utils.get_current_user)):
    return current_user
