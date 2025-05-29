import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_status():
    # Step 1: Create a task (approval not required, so it completes)
    payload = {
        "request": "Check system performance",
        "require_approval": False
    }

    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Step 2: Extract the task_id
    task_id = data.get("task_id")
    assert task_id is not None

    # ✅ Step 3: Call correct endpoint
    status_response = client.get(f"/api/v1/tasks/{task_id}")
    assert status_response.status_code == 200

    status_data = status_response.json()
    assert status_data["task_id"] == task_id
    assert status_data["status"] in ["completed", "waiting_approval", "resumed"]
