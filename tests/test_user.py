from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestUserSearchAPI:
    def test_user_valid_query(self):
        response = client.get("/user?datetime=20221104T1543&username=brainyHeron5")
        assert response.status_code == 200
        json = response.json()
        assert json["username"] == "brainyHeron5"

    def test_user_invalid_datetime_format(self):
        response = client.get("/user?username=brainyHeron5&datetime=2022-11-04T15:43")
        assert response.status_code == 422

    def test_user_missing_username(self):
        response = client.get("/user?datetime=20221104T1543")
        assert response.status_code == 422

    def test_user_nonexistent_user(self):
        response = client.get("/user?username=ghostPenguin999&datetime=20221104T1543")
        assert response.status_code == 200
        json = response.json()
        assert json["last24HourUsage"] == "0h00m"

    def test_user_future_datetime(self):
        response = client.get("/user?username=brainyHeron5&datetime=20300101T0000")
        assert response.status_code == 200
        json = response.json()
        assert json["last24HourUsage"] == "0h00m"
