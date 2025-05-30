# AI AutoPilot Agent Project

An agentic AI system built using FastAPI, LangGraph, DSPy, and OpenAI to process IT service requests end-to-end. The system uses a multi-agent architecture to handle task understanding, diagnostics, automation, and communication.

---

## 📊 Features

* **Multi-Agent Workflow**: Specialized agents like `CoordinatorAgent`, `DiagnosticAgent`, `AutomationAgent`, and `WriterAgent`.
* **LangGraph Integration**: For visual workflow execution and coordination.
* **DSPy Context Routing**: Efficient context pruning and routing with DSPy/MCP.
* **FastAPI Backend**: RESTful APIs for submitting tasks and querying task status.
* **Persistent Task Storage**: Integrated with SQLite/Postgres to store task history.
* **Approval Flow**: Tasks requiring approval are routed appropriately.
* **OpenAI LLM**: Handles language understanding, code generation, and summarization.

---

## 🚀 How to Run

1. Clone the repo

```bash
git clone https://github.com/SyamSundarAkina/AI_AutoPilot_Projects.git
cd AI_AutoPilot_Agent
```

2. Create a virtual environment and install dependencies

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set your environment variables

```bash
set OPENAI_API_KEY=your_openai_key
```

4. Run the app

```bash
uvicorn app.main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

---

## 🔧 API Endpoints

### POST `/task`

Submit a new task.

```json
{
  "request": "Diagnose why server xyz is slow and generate remediation steps",
  "require_approval": true
}
```

### GET `/status/{task_id}`

Get the current status and result of a submitted task.

---

## ✅ Testing

```bash
pytest tests/
```

Tests cover approval flow, retries, script generation, and task lifecycle.

---

## 🚜 Technologies Used

* FastAPI
* LangGraph
* DSPy/MCP
* OpenAI API
* Python 3.12+
* SQLite/Postgres
* Uvicorn

---

## 🚀 Future Enhancements

* Add user authentication and rate limiting
* Improve UI/UX with a React frontend
* Integrate with Microsoft Teams for notifications

---

## 🙏 Acknowledgments

Thanks to Open Source contributors of LangChain, LangGraph, DSPy, and FastAPI!
