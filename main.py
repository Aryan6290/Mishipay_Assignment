# internet-usage-service/main.py
from fastapi import FastAPI
from app.routers import analytics, user
import app.cache
app = FastAPI(title="Internet Usage Monitoring Service")

app.include_router(analytics.router, prefix="/analytics")
app.include_router(user.router, prefix="/user")