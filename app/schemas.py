
# app/schemas.py
from pydantic import BaseModel
from typing import List

class AnalyticsUser(BaseModel):
    username: str
    lastDayUsage: str
    last7DayUsage: str
    last30DayUsage: str

class AnalyticsResponse(BaseModel):
    ok: bool
    data: List[AnalyticsUser]
    pageSize: int
    page: int
    totalPages: int