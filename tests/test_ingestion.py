import pytest
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import UserUsage
from sqlalchemy import func

from ingestor.ingest_data import ingest_from_google_drive

@pytest.fixture(scope="function")
def db() -> Session:
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()

class TestIngestion:
    def test_ingestion_runs(self, db):
        # Run once
        

        # Run again to verify idempotency
        ingest_from_google_drive("14fVSrhg4ct9QWIAduvFR96zacPJdCy-_")

        count = db.query(func.count(UserUsage.id)).scalar()
        assert count > 0  # At least some rows must be ingested

    def test_fields_populated(self, db):
        record = db.query(UserUsage).first()
        assert record is not None
        assert isinstance(record.username, str)
        assert isinstance(record.mac_address, str)
        assert isinstance(record.start_time, object)
        assert isinstance(record.usage_seconds, int)
        assert record.upload_kb >= 0
        assert record.download_kb >= 0

    def test_no_duplicate_entries(self, db):
        count_1 = db.query(func.count(UserUsage.id)).scalar()
        ingest_from_google_drive("14fVSrhg4ct9QWIAduvFR96zacPJdCy-_")
        count_2 = db.query(func.count(UserUsage.id)).scalar()
        assert count_1 == count_2  # No new rows added
