from dspy import Module

class AgentRouter(Module):
    def __init__(self):
        super().__init__()

    def forward(self, input_request: str) -> str:
        input_lower = input_request.lower()
        if "diagnose" in input_lower or "cpu" in input_lower:
            return "diagnostic"
        elif "script" in input_lower or "powershell" in input_lower:
            return "automation"
        elif "summary" in input_lower or "email" in input_lower:
            return "writer"
        else:
            return "coordinator"
