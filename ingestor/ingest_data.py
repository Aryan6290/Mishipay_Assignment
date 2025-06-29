# ingest/ingest_data.py

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.db import SessionLocal, Base, engine
from app.models import UserUsage
from datetime import datetime
import requests
from io import StringIO
import os
import sys


import logging
logger = logging.getLogger(__name__)

# Allow import of app.db from parent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
Base.metadata.create_all(bind=engine)

def parse_duration(duration_str):
    h, m, s = map(int, duration_str.strip().split(":"))
    return h * 3600 + m * 60 + s

def ingest_from_google_drive(file_id: str):
    # Step 1: Download CSV
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code != 200:
        logger.error("Error in fetching csv from google drive")
        return

    df = pd.read_csv(StringIO(response.text))
    df.columns = df.columns.str.strip()

    # Step 2: Validate columns
    required = {'username', 'mac_address', 'start_time', 'usage_time', 'upload', 'download'}
    if not required.issubset(df.columns):
        logger.error(f"Missing columns - {required - set(df.columns)}")
        return

    # Step 3: Prepare data
    rows = []
    for _, row in df.iterrows():
        try:
            rows.append({
                "username": row["username"],
                "mac_address": row["mac_address"],
                "start_time": datetime.strptime(row["start_time"], "%Y-%m-%d %H:%M:%S"),
                "usage_seconds": parse_duration(row["usage_time"]),
                "upload_kb": float(row["upload"]),
                "download_kb": float(row["download"]),
            })
        except Exception as e:
            logger.error(f"❌ Skipping row due to error: {e}")

    if not rows:
        logger.error("⚠️ No valid rows to insert.")
        return

    # Step 4: Chunked insert using SessionLocal
    CHUNK_SIZE = 1000
    inserted_total = 0

    db: Session = SessionLocal()

    try:
        for i in range(0, len(rows), CHUNK_SIZE):
            chunk = rows[i:i + CHUNK_SIZE]

            stmt = insert(UserUsage).values(chunk)
            stmt = stmt.on_conflict_do_nothing(index_elements=["username", "mac_address", "start_time"])

            result = db.execute(stmt)
            inserted_total += result.rowcount

        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Bulk insert failed: {e}")
    finally:
        db.close()

    total_attempted = len(rows)
    duplicates = total_attempted - inserted_total

    logger.info(f"✅ Attempted: {total_attempted}")
    logger.info(f"✅ Inserted: {inserted_total}")
    logger.warning(f"⚠️ Duplicates Skipped: {duplicates}")

if __name__ == "__main__":
    file_id = "14fVSrhg4ct9QWIAduvFR96zacPJdCy-_"  # Replace with your file ID
    ingest_from_google_drive(file_id)
