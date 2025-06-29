# internet-usage-service/main.py
from fastapi import FastAPI
from app.routers import analytics, user

app = FastAPI(title="Internet Usage Monitoring Service")

app.include_router(analytics.router, prefix="/analytics")
app.include_router(user.router, prefix="/user")


# app/routers/analytics.py
from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from typing import List, Optional
from app.schemas import AnalyticsResponse, AnalyticsUser
from app.crud import get_top_users_by_usage

router = APIRouter()

@router.get("", response_model=AnalyticsResponse)
def get_analytics(
    date: str = Query(..., description="Date in DDMMYYYY format"),
    limit: int = Query(100, gt=0),
    page: int = Query(1, gt=0)
):
    try:
        reference_date = datetime.strptime(date, "%d%m%Y")
    except ValueError:
        raise HTTPException(status_code=422, detail="invalid date")

    users, total_pages = get_top_users_by_usage(reference_date, limit, page)

    return AnalyticsResponse(
        ok=True,
        data=users,
        pageSize=limit,
        page=page,
        totalPages=total_pages
    )