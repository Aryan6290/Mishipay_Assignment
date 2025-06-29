from pydantic import BaseModel
from typing import List


# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models import UserUsage
from app.db import SessionLocal
from datetime import datetime, timedelta
from app.schemas import AnalyticsUser, UserSummary
import math

from app.utils import format_duration



def get_top_users_by_usage(ref_date: datetime, limit: int, page: int):
    db: Session = SessionLocal()

    start_30 = ref_date - timedelta(days=30)
    start_7 = ref_date - timedelta(days=7)
    start_1 = ref_date - timedelta(days=1)

    subquery = (
        db.query(
            UserUsage.username,
            func.sum(
            case((UserUsage.start_time >= start_1, UserUsage.usage_seconds), else_=0)
            ).label("day1"),

            func.sum(
            case((UserUsage.start_time >= start_7, UserUsage.usage_seconds), else_=0)
            ).label("day7"),

            func.sum(
            case((UserUsage.start_time >= start_30, UserUsage.usage_seconds), else_=0)
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

def get_user_info(username: str , ref_time:datetime):
    db: Session = SessionLocal()
    username = username.strip()
    hour_1 = ref_time - timedelta(hours=1)
    hour_6 = ref_time - timedelta(hours=6)
    hour_24 = ref_time - timedelta(hours=24)

    results = db.query(
        func.sum(
            case((UserUsage.start_time >= hour_1, UserUsage.usage_seconds), else_=0)
        ).label("h1"),
        func.sum(
            case((UserUsage.start_time >= hour_6, UserUsage.usage_seconds), else_=0)
        ).label("h6"),
        func.sum(
            case((UserUsage.start_time >= hour_24, UserUsage.usage_seconds), else_=0)
        ).label("h24")
    ).filter(
        UserUsage.username == username,
        UserUsage.start_time <= ref_time,
        UserUsage.start_time >= hour_24
    ).first()

    db.close()

    return UserSummary(
        username=username,
        lastHourUsage=format_duration(results.h1),
        last6HourUsage=format_duration(results.h6),
        last24HourUsage=format_duration(results.h24)
    )

