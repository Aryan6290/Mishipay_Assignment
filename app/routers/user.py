from datetime import datetime as dt

from fastapi import APIRouter, HTTPException, Query
from app.schemas import UserSummary
from app.crud import  get_user_info
from aiocache import cached
router = APIRouter()

@cached(ttl=600)
@router.get("/search", response_model=UserSummary)
def get_analytics(
    datetime: str = Query(..., description="Date in DDMMYYYY format"),
    username: str = Query(None, description="(Optional) Filter by username"),
):
    try:
        reference_date = dt.strptime(datetime, "%Y%m%dT%H%M")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format. Use DDMMYYYY.")

    try:
        userinfo = get_user_info(username,reference_date)
    except Exception as e:
        raise HTTPException(status_code=422, detail="Check correct formatß")

    return userinfo