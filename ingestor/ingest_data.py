# ingestor/ingest_data.py

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import Base, SessionLocal, engine
from app.models import UserUsage
from datetime import datetime
import requests
from io import StringIO
import os
import sys

# Allow import of app.db from parent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
Base.metadata.create_all(bind=engine)
# Fixed file ID from Google Drive
GOOGLE_DRIVE_FILE_ID = "14fVSrhg4ct9QWIAduvFR96zacPJdCy-_"

def parse_duration(duration_str):
    h, m, s = map(int, duration_str.split(":"))
    return h * 3600 + m * 60 + s

def fetch_csv_from_drive(file_id: str) -> pd.DataFrame:
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"❌ Failed to download CSV. Status code: {response.status_code}")

    return pd.read_csv(StringIO(response.text))

def ingest_from_drive():
    df = fetch_csv_from_drive(GOOGLE_DRIVE_FILE_ID)

    required = {'username', 'mac_address', 'start_time', 'usage_time', 'upload', 'download'}
    df.columns = df.columns.str.strip() 
    if not required.issubset(df.columns):
        print("❌ Missing columns:", required - set(df.columns))
        print(df)
        return

    db: Session = SessionLocal()
    inserted, skipped = 0, 0

    for _, row in df.iterrows():
        try:
            record = UserUsage(
                username=row["username"],
                mac_address=row["mac_address"],
                start_time=datetime.strptime(row["start_time"], "%Y-%m-%d %H:%M:%S"),
                usage_seconds=parse_duration(row["usage_time"]),
                upload_kb=float(row["upload"]),
                download_kb=float(row["download"])
            )
            db.add(record)
            db.commit()
            inserted += 1
        except IntegrityError:
            db.rollback()
            skipped += 1
        except Exception as e:
            db.rollback()
            print(f"❌ Skipped row due to error: {e} {row}")

    db.close()
    print(f"✅ Ingest complete. Inserted: {inserted}, Skipped: {skipped} (duplicates or invalid rows)")

if __name__ == "__main__":
    ingest_from_drive()
