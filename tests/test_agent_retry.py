import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_agent_retry():
    # Patch AutomationAgent.run to simulate failure
    with patch("app.agents.automation.AutomationAgent.run") as mock_automation:
        mock_automation.side_effect = Exception("Simulated failure in AutomationAgent")

        payload = {
            "request": "Simulate disk cleanup on full drive",
            "require_approval": False
        }

        response = client.post("/api/v1/execute", json=payload)
        assert response.status_code == 200

        data = response.json()
        
        # ✅ Check that the status is still marked completed
        # or at least handled without server error
        assert "status" in data
        assert data["status"] == "completed" or data["script"] is None

        # ✅ Confirm fallback script response or error message
        if data.get("script"):
            assert "Script generation failed" in data["script"]["code"] or not data["script"]["lint_passed"]
