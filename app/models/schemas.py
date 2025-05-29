from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from enum import Enum


class MyModel(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class ApprovalStatus(str, Enum):
    waiting_approval = "waiting_approval"
    completed = "completed"
    failed = "failed"
    active = "active"


class ExecuteRequest(BaseModel):
    request: str
    require_approval: bool = False
    task_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DiagnosisSolution(BaseModel):
    title: str
    confidence: str

    model_config = ConfigDict(from_attributes=True)


class Diagnosis(BaseModel):
    root_cause: str
    evidence: List[str]
    solutions: List[DiagnosisSolution]

    model_config = ConfigDict(from_attributes=True)


class Script(BaseModel):
    language: str
    code: str
    lint_passed: bool

    model_config = ConfigDict(from_attributes=True)


class EmailDraft(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(BaseModel):
    task_id: str
    status: ApprovalStatus
    diagnosis: Optional[Diagnosis] = None
    script: Optional[Script] = None
    email_draft: Optional[str] = None
    duration_seconds: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
