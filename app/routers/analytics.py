from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from app.schemas import AnalyticsResponse
from app.crud import get_top_users_by_usage
from aiocache import cached
router = APIRouter()

@cached(ttl=600)
@router.get("", response_model=AnalyticsResponse)
def get_analytics(
    date: str = Query(..., description="Date in DDMMYYYY format"),
    limit: int = Query(100, gt=0),
    page: int = Query(1, gt=0)
):
    try:
        reference_date = datetime.strptime(date, "%d%m%Y")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format. Use DDMMYYYY.")

    users, total_pages = get_top_users_by_usage(reference_date, limit, page)

    return AnalyticsResponse(
        ok=True,
        data=users,
        pageSize=limit,
        page=page,
        totalPages=total_pages
    )