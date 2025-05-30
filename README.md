
# 🤖 AI Autopilot Agentic System

A LangGraph + FastAPI-based agentic system that automates IT troubleshooting tasks using multiple specialized agents. It handles request intake, diagnoses issues, executes remediation scripts, and optionally drafts email reports.

---

## 🚀 Features

- 🔁 **Coordinator Agent**: Orchestrates the flow across agents  
- 🧠 **Diagnostic Agent**: Uses LLM to analyze issue descriptions  
- 🤖 **Automation Agent**: Generates platform-specific remediation scripts  
- ✍️ **Writer Agent**: Drafts executive summary emails for results  
- 🔐 **Approval Flow**: Optional human-in-the-loop before actions  
- 🛠️ **Retry Logic**: Automatically retries failed agent calls  
- ✅ **Test Coverage**: Multiple Pytest scenarios for all endpoints

---

## 📈 Fine-Tuning Workflow

<img src="" alt="Workflow Diagram" width="300"/>

## 🗂️ Folder Structure

```

AI\_AutoPilot\_Agent/
├── app/
│   ├── agents/               # Coordinator, Diagnostic, Automation, Writer
│   ├── api/                  # FastAPI route handlers
│   ├── services/             # LLM and agent routing logic
│   └── main.py               # App entry point
│
├── tests/                    # Pytest-based test suite
│   ├── test\_happy\_path.py
│   ├── test\_approval\_flow\.py
│   ├── test\_get\_status.py
│   ├── test\_script\_compiles.py
│   └── test\_agent\_retry.py
│
├── requirements.txt
└── README.md

````

---

## 🧪 Run the App

```bash
uvicorn app.main:app --reload
````

Once started, open:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📝 Example Swagger Requests

### ✅ Happy Path (Auto-execution)

```json
POST /api/v1/execute
{
  "request": "Diagnose why Windows Server 2019 VM cpu01 hits 95%+ CPU, generate a PowerShell script to collect perfmon logs, and draft an email to management summarizing findings.",
  "require_approval": false
}
```

### 🔐 Approval Path

```json
POST /api/v1/execute
{
  "request": "Diagnose root cause of network latency for Linux VM `net-app-01`, suggest fixes, and generate Bash script to flush firewall and renew DHCP.",
  "require_approval": true
}
```

Then approve:

```http
POST /api/v1/plans/{task_id}/approve
```

---

## 🧪 Testing the System

Run the full test suite:

```bash
pytest tests/
```

### Test Breakdown

| Test File                 | Purpose                                              |
| ------------------------- | ---------------------------------------------------- |
| `test_happy_path.py`      | Full flow with no approval needed                    |
| `test_approval_flow.py`   | Test approve & reject endpoints                      |
| `test_get_status.py`      | Confirm status polling reflects real-time state      |
| `test_script_compiles.py` | Validate generated PowerShell/Bash scripts are valid |
| `test_agent_retry.py`     | Simulates AutomationAgent failure and verifies retry |

---

## 🔁 Retry Logic

If any agent (e.g., `AutomationAgent`) throws a transient error, retry logic kicks in automatically. This ensures:

* No manual restarts needed
* Task execution continues when transient errors (e.g., API hiccups) resolve
* Observability via logs and test coverage

---

## 🛠 Tech Stack

* **LLM**: OpenAI GPT-4 (via Python SDK)
* **Framework**: FastAPI + Uvicorn
* **Orchestration**: LangGraph + DSPy/MCP
* **Testing**: Pytest
* **Persistence**: In-memory dict or file-based storage (can plug in DB)

---

## 🔐 Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key
```

---

## 📦 Installation

```bash
git clone https://github.com/SyamSundarAkina/AI_AutoPilot_Projects.git
cd AI_AutoPilot_Projects
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📄 License

Licensed under the [MIT License](LICENSE).
Feel free to use, modify, and build on this project!

```


