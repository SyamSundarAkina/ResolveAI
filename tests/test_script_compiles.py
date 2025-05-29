import subprocess
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("shell", ["bash", "powershell"])
def test_script_compiles(shell):
    payload = {
        "request": "Clean up temporary files and logs",
        "require_approval": False
    }

    response = client.post("/api/v1/execute", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "completed"
    assert "script" in data
    script = data["script"]["code"]
    language = data["script"]["language"].lower()

    if shell == "bash" and "bash" in language:
        with open("temp_script.sh", "w") as f:
            f.write(script)
        result = subprocess.run(["bash", "-n", "temp_script.sh"], capture_output=True, text=True)
        assert result.returncode == 0, f"Bash syntax error: {result.stderr}"

    elif shell == "powershell" and "powershell" in language:
        with open("temp_script.ps1", "w") as f:
            f.write(script)
        result = subprocess.run(["powershell.exe", "-Command", f".\\temp_script.ps1"], capture_output=True, text=True)
        assert result.returncode == 0, f"PowerShell execution failed: {result.stderr}"

