from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from app.db import Base

class UserUsage(Base):
    __tablename__ = "user_usage"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    mac_address = Column(String, index=True)
    start_time = Column(DateTime, index=True)
    usage_seconds = Column(Integer)
    upload_kb = Column(Float)
    download_kb = Column(Float)

    __table_args__ = (
        UniqueConstraint("username", "mac_address", "start_time", name="uq_usage_entry"),
    )

    # This is used that same data is not ingested.
