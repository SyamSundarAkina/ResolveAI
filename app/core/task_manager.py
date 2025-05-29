from typing import Dict, Optional, Any
from threading import Lock

# Simulated in-memory task store (you can replace this with a DB later)
task_store: Dict[str, Dict[str, Any]] = {}
lock = Lock()

def save_task(task_id: str, data: Dict[str, Any]) -> None:
    with lock:
        task_store[task_id] = data

def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    with lock:
        return task_store.get(task_id)

# Alias for compatibility (e.g., if older code uses 'load_task')
load_task = get_task

def update_task_status(task_id: str, status: str) -> None:
    with lock:
        if task_id in task_store:
            task_store[task_id]["status"] = status

