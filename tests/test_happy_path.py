import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_happy_path():
    payload = {
        "request": "Disk space full on production server",
        "require_approval": False
    }

    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200

    data = response.json()

    # Basic structure validation
    assert data["status"] == "completed"
    assert data["task_id"] is not None

    # Diagnosis section
    diagnosis = data.get("diagnosis")
    assert diagnosis is not None
    assert "root_cause" in diagnosis and diagnosis["root_cause"]
    assert "evidence" in diagnosis and len(diagnosis["evidence"]) > 0
    assert "solutions" in diagnosis and len(diagnosis["solutions"]) > 0

    # Script section
    script = data.get("script")
    assert script is not None
    assert script["language"] in ["powershell", "bash"]
    assert script["code"] and isinstance(script["code"], str)

    # Optional: validate email draft exists
    assert "email_draft" in data and data["email_draft"]

    print("✅ test_happy_path passed.")
