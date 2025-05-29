from app.agents.base_agent import BaseAgent
from app.services.llm import call_llm

class KnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__("KnowledgeAgent")

    def run(self, request: str) -> dict:
        self.log("Answering with general knowledge via LLM")

        prompt = f"""
You are a helpful AI assistant with access to general IT and business knowledge.

User Request:
{request}

Please provide a clear, informative, and helpful answer using your general knowledge.
"""

        answer = call_llm(prompt)
        return {"answer": answer.strip()}
# This agent uses an LLM to provide answers based on general knowledge.
# It expects the LLM to return a plain text response.

