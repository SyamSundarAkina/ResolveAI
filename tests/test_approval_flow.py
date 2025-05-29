import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_approval_flow():
    # Step 1: Submit a request that requires approval
    payload = {
        "request": "CRM app is responding slowly after update",
        "require_approval": True
    }
    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "waiting_approval"
    assert "task_id" in data
    task_id = data["task_id"]

    # Step 2: Approve the task
    approve_response = client.post(f"/api/v1/plans/{task_id}/approve")
    assert approve_response.status_code == 200

    # Step 3: Fetch the final task status
    final_response = client.get(f"/api/v1/tasks/{task_id}")
    assert final_response.status_code == 200

    final_data = final_response.json()
    assert final_data["status"] == "completed"
    assert final_data["diagnosis"] is not None
    assert final_data["script"] is not None
    assert final_data["email_draft"] is not None
