from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from app.schemas import UserSummary
from app.crud import  get_user_info

router = APIRouter()

@router.get("", response_model=UserSummary)
def get_analytics(
    date: str = Query(..., description="Date in DDMMYYYY format"),
    username: str = Query(None, description="(Optional) Filter by username"),
):
    try:
        reference_date = datetime.strptime(date, "%d%m%Y")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format. Use DDMMYYYY.")

    userinfo = get_user_info(username,reference_date)

    return userinfo