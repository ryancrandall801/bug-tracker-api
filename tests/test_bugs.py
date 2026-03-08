from fastapi.testclient import TestClient
from app.main import app
from app.routes import bugs as bugs_module

client = TestClient(app)


def reset_bug_store():
    bugs_module.bugs_db.clear()
    bugs_module.next_bug_id = 1


def test_create_bug_success():
    reset_bug_store()

    payload = {
        "title": "Login button not working",
        "description": "Clicking login does nothing",
        "priority": "high",
    }

    response = client.post("/bugs", json=payload)

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["priority"] == payload["priority"]
    assert response.json()["status"] == "open"


def test_create_bug_missing_title():
    reset_bug_store()

    payload = {
        "description": "Missing title field",
        "priority": "high",
    }

    response = client.post("/bugs", json=payload)

    assert response.status_code == 422


def test_get_bugs_returns_created_bugs():
    reset_bug_store()

    client.post(
        "/bugs",
        json={
            "title": "First bug",
            "description": "First description",
            "priority": "medium",
        },
    )
    client.post(
        "/bugs",
        json={
            "title": "Second bug",
            "description": "Second description",
            "priority": "high",
        },
    )

    response = client.get("/bugs")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "First bug"
    assert response.json()[1]["title"] == "Second bug"


def test_get_bug_by_id_returns_correct_bug():
    reset_bug_store()

    create_response = client.post(
        "/bugs",
        json={
            "title": "Find me",
            "description": "Specific bug",
            "priority": "low",
        },
    )

    bug_id = create_response.json()["id"]

    response = client.get(f"/bugs/{bug_id}")

    assert response.status_code == 200
    assert response.json()["id"] == bug_id
    assert response.json()["title"] == "Find me"


def test_get_bug_by_id_returns_404_for_missing_bug():
    reset_bug_store()

    response = client.get("/bugs/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Bug with id 999 not found"}

def test_patch_bug_updates_status():
    reset_bug_store()

    create_response = client.post(
        "/bugs",
        json={
            "title": "Status bug",
            "description": "Needs update",
            "priority": "medium",
        },
    )

    bug_id = create_response.json()["id"]

    response = client.patch(
        f"/bugs/{bug_id}",
        json={"status": "resolved"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == bug_id
    assert response.json()["status"] == "resolved"
    assert response.json()["title"] == "Status bug"


def test_patch_bug_updates_multiple_fields():
    reset_bug_store()

    create_response = client.post(
        "/bugs",
        json={
            "title": "Old title",
            "description": "Old description",
            "priority": "low",
        },
    )

    bug_id = create_response.json()["id"]

    response = client.patch(
        f"/bugs/{bug_id}",
        json={
            "title": "New title",
            "priority": "critical",
            "status": "in_progress",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["priority"] == "critical"
    assert response.json()["status"] == "in_progress"
    assert response.json()["description"] == "Old description"


def test_patch_bug_returns_404_for_missing_bug():
    reset_bug_store()

    response = client.patch(
        "/bugs/999",
        json={"status": "closed"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Bug with id 999 not found"}


def test_patch_bug_rejects_invalid_status():
    reset_bug_store()

    create_response = client.post(
        "/bugs",
        json={
            "title": "Validation bug",
            "description": "Try invalid status",
            "priority": "high",
        },
    )

    bug_id = create_response.json()["id"]

    response = client.patch(
        f"/bugs/{bug_id}",
        json={"status": "done"},
    )

    assert response.status_code == 422


def test_delete_bug_success():
    reset_bug_store()

    create_response = client.post(
        "/bugs",
        json={
            "title": "Delete me",
            "description": "Temporary bug",
            "priority": "medium",
        },
    )

    bug_id = create_response.json()["id"]

    delete_response = client.delete(f"/bugs/{bug_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/bugs/{bug_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": f"Bug with id {bug_id} not found"}


def test_delete_bug_returns_404_for_missing_bug():
    reset_bug_store()

    response = client.delete("/bugs/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Bug with id 999 not found"}


def test_delete_bug_is_idempotent_in_system_state():
    reset_bug_store()

    create_response = client.post(
        "/bugs",
        json={
            "title": "Delete twice",
            "description": "Testing idempotency",
            "priority": "high",
        },
    )

    bug_id = create_response.json()["id"]

    first_delete = client.delete(f"/bugs/{bug_id}")
    second_delete = client.delete(f"/bugs/{bug_id}")
    final_get = client.get(f"/bugs/{bug_id}")

    assert first_delete.status_code == 204
    assert second_delete.status_code == 404
    assert final_get.status_code == 404

def test_get_bugs_filters_by_status():
    reset_bug_store()

    first_response = client.post(
        "/bugs",
        json={
            "title": "Open bug",
            "description": "Still open",
            "priority": "medium",
        },
    )

    second_response = client.post(
        "/bugs",
        json={
            "title": "Resolved bug",
            "description": "Already fixed",
            "priority": "high",
        },
    )

    second_bug_id = second_response.json()["id"]

    client.patch(
        f"/bugs/{second_bug_id}",
        json={"status": "resolved"},
    )

    response = client.get("/bugs?status=resolved")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Resolved bug"
    assert response.json()[0]["status"] == "resolved"


def test_get_bugs_filters_by_priority():
    reset_bug_store()

    client.post(
        "/bugs",
        json={
            "title": "Low priority bug",
            "description": "Minor issue",
            "priority": "low",
        },
    )

    client.post(
        "/bugs",
        json={
            "title": "Critical bug",
            "description": "Major issue",
            "priority": "critical",
        },
    )

    response = client.get("/bugs?priority=critical")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Critical bug"
    assert response.json()[0]["priority"] == "critical"


def test_get_bugs_filters_by_status_and_priority():
    reset_bug_store()

    first_response = client.post(
        "/bugs",
        json={
            "title": "Open high bug",
            "description": "Should match both filters",
            "priority": "high",
        },
    )

    second_response = client.post(
        "/bugs",
        json={
            "title": "Resolved high bug",
            "description": "Should not match open filter",
            "priority": "high",
        },
    )

    client.post(
        "/bugs",
        json={
            "title": "Open low bug",
            "description": "Should not match high filter",
            "priority": "low",
        },
    )

    second_bug_id = second_response.json()["id"]

    client.patch(
        f"/bugs/{second_bug_id}",
        json={"status": "resolved"},
    )

    response = client.get("/bugs?status=open&priority=high")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Open high bug"
    assert response.json()[0]["status"] == "open"
    assert response.json()[0]["priority"] == "high"


def test_get_bugs_filter_returns_empty_list_when_no_matches():
    reset_bug_store()

    client.post(
        "/bugs",
        json={
            "title": "Only low bug",
            "description": "No critical bug exists",
            "priority": "low",
        },
    )

    response = client.get("/bugs?priority=critical")

    assert response.status_code == 200
    assert response.json() == []