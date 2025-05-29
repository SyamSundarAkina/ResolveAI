from fastapi import APIRouter
from app.models.schemas import ExecuteRequest, TaskResponse
from app.agents.coordinator import CoordinatorAgent

router = APIRouter()
coordinator = CoordinatorAgent()

# POST endpoint to trigger agent execution
@router.post("/execute", response_model=TaskResponse)
def execute_task(payload: ExecuteRequest):
    """
    Accepts an input text with an optional approval flag, and returns the result after planning and execution.
    """
    response = coordinator.plan_and_execute(payload)
    return response

# Optional: Simple GET endpoint for health check
@router.get("/execute")
async def check_execute():
    return {"message": "Execute endpoint is live"}
