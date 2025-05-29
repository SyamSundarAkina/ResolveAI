
from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from app.core.task_manager import get_task

router = APIRouter()

@router.get("/tasks/{task_id}", response_model=Dict[str, Any])
def get_task_status(task_id: str):
    """
    Retrieve the full task record (status, input, partial or final results).
    """
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
