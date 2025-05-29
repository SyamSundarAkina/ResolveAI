from app.agents.base_agent import BaseAgent
from app.services.llm import call_llm


class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("WriterAgent")

    def run(self, inputs: dict) -> dict:
        self.log("Writing email draft from diagnosis and script")

        root_cause = inputs.get("root_cause", "an unknown issue")
        evidence = inputs.get("evidence", [])
        script = inputs.get("script", "")

        prompt = (
            "You are an IT support assistant. Based on the root cause, evidence, and script below, write a professional email draft to the internal IT team.\n"
            "Include bullet points for evidence and paste the script as a code block.\n\n"
            f"Root Cause: {root_cause}\n"
            f"Evidence: {evidence}\n"
            f"Script: {script}\n\n"
            "Respond in this format:\n"
            "{ \"content\": \"...\" }"
        )

        response = call_llm(prompt)

        try:
            result = eval(response)
            return result
        except Exception:
            self.log("Failed to parse LLM response. Returning fallback email.")
            return {
                "content": (
                    "Hello team,\n\nWe encountered an issue but could not generate a proper diagnosis. "
                    "Please manually check the system.\n\nRegards,\nAI Assistant"
                )
            }
