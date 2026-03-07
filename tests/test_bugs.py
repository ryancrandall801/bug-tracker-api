from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_bug_success():
    payload = {
        "title": "Login button not working",
        "description": "Clicking login does nothing",
        "priority": "high",
    }

    response = client.post("/bugs", json=payload)

    assert response.status_code == 201
    assert response.json()["id"] >= 1
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["priority"] == payload["priority"]
    assert response.json()["status"] == "open"


def test_create_bug_missing_title():
    payload = {
        "description": "Missing title field",
        "priority": "high",
    }

    response = client.post("/bugs", json=payload)

    assert response.status_code == 422