# Internet Usage Analytics Service

This is a FastAPI-based backend service that ingests internet usage data from a CSV file and provides endpoints for usage analytics and user-specific summaries. It is designed with modular architecture, PostgreSQL integration, caching, and test coverage.

## Features

- One-time ingestion from a public CSV (Google Drive)
- PostgreSQL + SQLAlchemy ORM
- FastAPI with class-based route handlers
- Endpoints:
  - `/analytics`: Aggregated user usage for 1/7/30 days
  - `/user/search`: Single user usage for last 1/6/24 hours
- Query parameter validation and pagination support
- In-memory caching using `aiocache`
- Pytest-based test suite with ingestion flag

## Project Structure


![image](https://github.com/user-attachments/assets/b972c685-f29e-46fd-926a-71581453667b)


## Requirements

- Python 3.9+
- PostgreSQL database or cloud equivalent (e.g. Neon)
- Redis (optional, for production caching)

## Setup

```bash
git clone https://github.com/<your-username>/<repo>.git
cd <repo>
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- Set your DB URL:

```bash
export DATABASE_URL=postgresql://<user>:<pass>@<host>/<dbname>
```
-Run the Service
```
uvicorn app.main:app --reload
- For API Docs:
Swagger: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```
- Run Tests
```
pytest --ingest     # Ingests CSV once before test session
pytest              # Run without ingestion
```
