
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

class UserSummary(BaseModel):
    username: str
    lastHourUsage: str
    last6HourUsage: str
    last24HourUsage: str

class UserSearchResponse(BaseModel):
    ok: bool
    data: UserSummary