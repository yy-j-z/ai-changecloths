from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/internal/v1/health")

    assert response.status_code == 200
    assert response.json()["data"]["service"] == "ai"


def test_size_recommendation() -> None:
    response = client.post(
        "/internal/v1/size/recommend",
        json={"height_cm": 170, "weight_kg": 65},
    )

    assert response.status_code == 200
    assert response.json()["data"]["size"] == "M"


def test_size_rejects_invalid_height() -> None:
    response = client.post(
        "/internal/v1/size/recommend",
        json={"height_cm": 0, "weight_kg": 65},
    )

    assert response.status_code == 422
