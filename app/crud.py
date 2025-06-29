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


# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_
from app.models import UserUsage
from app.db import SessionLocal
from datetime import datetime, timedelta
from app.schemas import AnalyticsUser
import math


def format_duration(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h{minutes:02d}m"


def get_top_users_by_usage(ref_date: datetime, limit: int, page: int):
    db: Session = SessionLocal()

    start_30 = ref_date - timedelta(days=30)
    start_7 = ref_date - timedelta(days=7)
    start_1 = ref_date - timedelta(days=1)

    subquery = (
        db.query(
            UserUsage.username,
            func.sum(
                case([(UserUsage.start_time >= start_1, UserUsage.usage_seconds)], else_=0)
            ).label("day1"),
            func.sum(
                case([(UserUsage.start_time >= start_7, UserUsage.usage_seconds)], else_=0)
            ).label("day7"),
            func.sum(
                case([(UserUsage.start_time >= start_30, UserUsage.usage_seconds)], else_=0)
            ).label("day30")
        )
        .filter(UserUsage.start_time >= start_30, UserUsage.start_time <= ref_date)
        .group_by(UserUsage.username)
        .subquery()
    )

    query = db.query(
        subquery.c.username,
        subquery.c.day1,
        subquery.c.day7,
        subquery.c.day30
    ).order_by(subquery.c.day30.desc())

    total_users = query.count()
    total_pages = math.ceil(total_users / limit)

    results = query.offset((page - 1) * limit).limit(limit).all()
    db.close()

    users = [
        AnalyticsUser(
            username=row.username,
            lastDayUsage=format_duration(row.day1),
            last7DayUsage=format_duration(row.day7),
            last30DayUsage=format_duration(row.day30),
        )
        for row in results
    ]

    return users, total_pages
