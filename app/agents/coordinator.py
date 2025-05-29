import uuid
import time
from app.models.schemas import (
    ExecuteRequest,
    TaskResponse,
    Diagnosis,
    Script,
    EmailDraft,
    ApprovalStatus
)
from app.agents.diagnostic import DiagnosticAgent
from app.agents.automation import AutomationAgent
from app.agents.writer import WriterAgent
from app.agents.knowledge import KnowledgeAgent
from app.services.router_dspy import AgentRouter
from app.services.context_pruner import prune_input_context
from app.core.task_manager import get_task, save_task, update_task_status

class CoordinatorAgent:
    def __init__(self):
        self.diagnostic_agent = DiagnosticAgent()
        self.automation_agent = AutomationAgent()
        self.writer_agent = WriterAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.router = AgentRouter()

    def plan_and_execute(self, request_data: ExecuteRequest, resume: bool = False) -> TaskResponse:
        task_id = request_data.task_id or str(uuid.uuid4())
        start_time = time.time()

        # ✂️ Prune context using MCP
        pruned_input = prune_input_context(request_data.request)

        # 🧠 Use DSPy/MCP to route
        route = self.router.forward(pruned_input)
        print(f"[Router] Routed to: {route}")

        # 👉 Route to Knowledge Agent if informational query
        if route == "KnowledgeAgent":
            knowledge_result = self.knowledge_agent.run(pruned_input)
            update_task_status(task_id, "completed")
            return TaskResponse(
                task_id=task_id,
                status=ApprovalStatus.completed,
                diagnosis=None,
                script=None,
                email_draft=knowledge_result["answer"],
                duration_seconds=int(time.time() - start_time)
            )

        # 1. Diagnostic
        diagnosis_result = self.diagnostic_agent.run(pruned_input)
        diagnosis = Diagnosis(
            root_cause=diagnosis_result["root_cause"],
            evidence=diagnosis_result["evidence"],
            solutions=diagnosis_result["solutions"]
        )

        # Pause if approval required
        if request_data.require_approval and not resume:
            save_task(task_id, {
                "input": request_data.model_dump(),
                "status": "waiting_approval",
                "partial_result": diagnosis.model_dump()
            })
            return TaskResponse(
                task_id=task_id,
                status=ApprovalStatus.waiting_approval,
                diagnosis=diagnosis,
                script=None,
                email_draft=None,
                duration_seconds=0
            )
        else:
            update_task_status(task_id, "resumed")

        # 2. Automation (with failure handling)
        try:
            script_result = self.automation_agent.run(pruned_input)
            script = Script(
                language=script_result["language"],
                code=script_result["code"],
                lint_passed=script_result["lint_passed"]
            )
        except Exception as e:
            update_task_status(task_id, "failed")
            return TaskResponse(
                task_id=task_id,
                status=ApprovalStatus.failed,
                diagnosis=diagnosis,
                script=None,
                email_draft=f"Automation failed: {str(e)}",
                duration_seconds=int(time.time() - start_time)
       )

        # 3. Writer
        email_result = self.writer_agent.run({
            "root_cause": diagnosis.root_cause,
            "evidence": diagnosis.evidence,
            "script": script.code
        })
        email = EmailDraft(content=email_result["content"])

        end_time = time.time()

        update_task_status(task_id, "completed")

        return TaskResponse(
            task_id=task_id,
            status=ApprovalStatus.completed,
            diagnosis=diagnosis,
            script=script,
            email_draft=email.content,
            duration_seconds=int(end_time - start_time)
        )

    # ✅ Async wrapper to allow resumable workflows
    async def run(self, input_text: dict, resume: bool = False) -> TaskResponse:
        request = ExecuteRequest(**input_text)
        return self.plan_and_execute(request, resume=resume)
