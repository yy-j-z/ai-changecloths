from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_advisor_asks_for_missing_scene() -> None:
    response = client.post("/api/v1/assistant/chat", json={"message": "帮我搭一身衣服"})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["state"] == "needs_input"
    assert data["tool_events"] == []


def test_advisor_calls_tools_and_returns_outfit_action() -> None:
    response = client.post(
        "/api/v1/assistant/chat",
        json={
            "message": "我下周面试，预算800元，想正式但不要黑色",
            "user_height_cm": 170,
            "user_weight_kg": 65,
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["state"] == "completed"
    assert [event["tool"] for event in data["tool_events"]] == [
        "search_products",
        "recommend_size",
        "check_outfit_compatibility",
        "apply_outfit",
    ]
    assert data["outfit_action"]["garment_id"] == "garment-jacket-001"
    assert data["outfit_action"]["size"] == "M"


def test_advisor_uses_history_for_multi_turn_context() -> None:
    response = client.post(
        "/api/v1/assistant/chat",
        json={
            "conversation_id": "demo-session",
            "message": "预算500，简约一点",
            "history": [
                {"role": "user", "content": "我要准备面试"},
                {"role": "assistant", "content": "你的预算和风格偏好是什么？"},
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["state"] == "completed"


def test_advisor_relaxes_budget_when_no_products_match() -> None:
    # 聚会场景只有 T 恤(¥159)，预算 100 首次查不到，放宽后应找到
    response = client.post(
        "/api/v1/assistant/chat",
        json={
            "message": "我要去聚会，预算100元",
            "user_height_cm": 170,
            "user_weight_kg": 65,
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["state"] == "completed"
    search_events = [e for e in data["tool_events"] if e["tool"] == "search_products"]
    assert len(search_events) >= 2
    assert "放宽预算" in search_events[1]["label"]
    assert data["outfit_action"]["garment_id"] == "garment-tee-001"


def test_advisor_relaxes_style_when_budget_still_empty() -> None:
    # 面试场景衬衫¥299/夹克¥499，预算100放宽到200仍查不到，再放宽风格后找到
    response = client.post(
        "/api/v1/assistant/chat",
        json={
            "message": "我下周面试，预算100，要正式",
            "user_height_cm": 170,
            "user_weight_kg": 65,
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["state"] == "completed"
    search_events = [e for e in data["tool_events"] if e["tool"] == "search_products"]
    assert len(search_events) == 3
    assert "放宽风格" in search_events[2]["label"]
