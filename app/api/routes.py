from fastapi import APIRouter, HTTPException, Path
from app.agents.coordinator import CoordinatorAgent
from app.models.schemas import ExecuteRequest, TaskResponse
from app.core.task_manager import save_task, get_task, update_task_status

router = APIRouter()
coordinator = CoordinatorAgent()

# 🔁 POST /execute - Process new requests
@router.post("/execute", response_model=TaskResponse)
async def execute_request(request: ExecuteRequest):
    result = await coordinator.run(request.model_dump())

    save_task(result.task_id, {
        "input": request.model_dump(),
        "status": result.status,
        "result": result.model_dump() if result.status == "completed" else {},
        "partial_result": result.model_dump() if result.status == "waiting_approval" else {}
    })

    return result

# ✅ POST /plans/{id}/approve - Approve a pending plan
@router.post("/plans/{task_id}/approve", response_model=TaskResponse)
async def approve_task(task_id: str = Path(...)):
    task_data = get_task(task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data["status"] != "waiting_approval":
        raise HTTPException(status_code=400, detail="Task is not waiting for approval")

    result = await coordinator.run(task_data["input"], resume=True)

    save_task(task_id, {
        "input": task_data["input"],
        "status": "completed",
        "result": result.model_dump()
    })

    return result

# ❌ POST /plans/{id}/reject - Reject a pending plan
@router.post("/plans/{task_id}/reject")
async def reject_task(task_id: str = Path(...)):
    task_data = get_task(task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data["status"] != "waiting_approval":
        raise HTTPException(status_code=400, detail="Task is not waiting for approval")

    update_task_status(task_id, "failed")

    return {
        "message": f"Task {task_id} has been rejected.",
        "status": "failed"
    }

# 📊 GET /tasks/{id} - Get task status and results
@router.get("/tasks/{task_id}", response_model=dict)
def get_status(task_id: str = Path(...)):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] == "completed" and "result" in task:
        return task["result"]

    return task

