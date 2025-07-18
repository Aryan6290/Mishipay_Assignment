# internet-usage-service/main.py
from fastapi import FastAPI
from app.routers import analytics, user
import app.cache
from app.utils.logging import configure_logging

app = FastAPI(title="Internet Usage Monitoring Service")



configure_logging()

app.include_router(analytics.router, prefix="/analytics")
app.include_router(user.router, prefix="/user")