from app.agents.base_agent import BaseAgent
from app.services.llm import call_llm


class DiagnosticAgent(BaseAgent):
    def __init__(self):
        super().__init__("DiagnosticAgent")

    def run(self, request: str) -> dict:
        self.log("Diagnosing issue from request")

        prompt = (
            "You are an expert system administrator. Based on the input below, identify:\n"
            "1. The root cause of the issue\n"
            "2. Two key evidence points\n"
            "3. Two recommended solutions with confidence levels (high/medium/low).\n\n"
            f"Input: {request}\n\n"
            "Respond in the following JSON format:\n"
            "{\n"
            "  \"root_cause\": \"...\",\n"
            "  \"evidence\": [\"...\", \"...\"],\n"
            "  \"solutions\": [\n"
            "    {\"title\": \"...\", \"confidence\": \"high\"},\n"
            "    {\"title\": \"...\", \"confidence\": \"medium\"}\n"
            "  ]\n"
            "}"
        )

        response = call_llm(prompt)

        try:
            # Evaluate the string as a dictionary (secure JSON parsing recommended in production)
            result = eval(response)
            return result
        except Exception:
            self.log("Failed to parse LLM response. Returning fallback.")
            return {
                "root_cause": "Unable to determine",
                "evidence": ["Input unclear", "Parsing error"],
                "solutions": [{"title": "Review input", "confidence": "low"}]
            }
