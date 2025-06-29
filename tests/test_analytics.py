from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAnalyticsAPI:
    def test_analytics_success(self):
        response = client.get("/analytics?date=04112022&limit=5&page=1")
        assert response.status_code == 200
        json = response.json()
        assert json["ok"] is True
        assert "data" in json
        assert isinstance(json["data"], list)

    def test_analytics_invalid_date(self):
        response = client.get("/analytics?date=04-11-2022")
        assert response.status_code == 422

    def test_analytics_current_date(self):
        # assuming there's no data on this future date
        response = client.get("/analytics?date=29062025")
        assert response.status_code == 200
        assert len(response.json()["data"]) == 0
