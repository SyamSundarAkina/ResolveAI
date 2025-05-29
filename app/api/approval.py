from fastapi import APIRouter, HTTPException
from app.core.task_manager import get_task, update_task_status, save_task
from app.agents.coordinator import CoordinatorAgent
from app.models.schemas import ExecuteRequest

router = APIRouter()
coordinator = CoordinatorAgent()

@router.post("/plans/{task_id}/approve")
async def approve_task(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.get("status") != "waiting_approval":
        raise HTTPException(status_code=400, detail="Task is not waiting for approval")

    if "input" not in task:
        raise HTTPException(status_code=400, detail="Task input missing")

    # Update status to approved
    update_task_status(task_id, "approved")

    # Resume the full task execution
    resumed_result = coordinator.plan_and_execute(
        ExecuteRequest(**task["input"]),
        resume=True
    )

    # Save the final output to the task store
    save_task(task_id, resumed_result.model_dump())

    return {"status": "resumed", "result": resumed_result}


@router.post("/plans/{task_id}/reject")
async def reject_task(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_task_status(task_id, "rejected")
    return {"status": "rejected"}
