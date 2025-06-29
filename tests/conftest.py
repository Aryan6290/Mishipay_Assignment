import pytest
from fastapi.testclient import TestClient

import app
from ingestor.ingest_data import ingest_from_google_drive

import logging
logger = logging.getLogger(__name__)

# ✅ Custom pytest CLI flag: --ingest
def pytest_addoption(parser):
    parser.addoption(
        "--ingest", action="store_true", default=False,
        help="Run ingestion before executing tests"
    )

# ✅ One-time ingestion fixture, only runs if --ingest is passed
@pytest.fixture(scope="session", autouse=True)
def one_time_ingestion(request):
    if request.config.getoption("--ingest"):
        logger.info("🔁 [conftest] Running one-time ingestion...")
        ingest_from_google_drive("14fVSrhg4ct9QWIAduvFR96zacPJdCy-_")
    else:
        logger.warn("⚠️  [conftest] Skipping ingestion (pass --ingest to enable)")

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

