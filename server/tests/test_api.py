from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["data"]["service"] == "server"


def test_avatar_defaults_follow_normalized_contract() -> None:
    response = client.get("/api/v1/avatars/defaults")

    assert response.status_code == 200
    body = response.json()["data"]["body"]
    assert all(0 <= value <= 1 for value in body.values())
