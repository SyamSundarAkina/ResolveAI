from app.agents.base_agent import BaseAgent
from app.services.llm import call_llm


class AutomationAgent(BaseAgent):
    def __init__(self):
        super().__init__("AutomationAgent")

    def run(self, request: str) -> dict:
        self.log("Generating remediation script and email draft")

        if not request or len(request.strip()) < 10:
            return {
                "language": "powershell",
                "code": "Write-Output 'Request too vague to generate a script.'",
                "lint_passed": False,
                "email_draft": "The issue description provided is too vague to generate an appropriate script or email. Please provide more context."
            }

        # Prompt to generate PowerShell script
        script_prompt = f"""
You are an expert IT assistant. Based on the following issue, generate a PowerShell script that attempts to fix the problem. Avoid just diagnostics; the script must take **corrective action** (e.g., delete logs, restart service, clean temp files).

Issue: {request}

Instructions:
- Output ONLY the PowerShell script, no comments or explanations.
- Do not include markdown formatting like ```powershell.

Begin the script directly:
"""

        # Prompt to generate email
        email_prompt = f"""
You are an AI IT Support Assistant. Based on the following system issue, write a professional email draft to notify the IT team. Mention the symptoms, suggest urgency, and describe the action steps (such as using the script). Keep the tone professional.

Issue: {request}

Email format:
- Subject line
- Proper greeting
- Description of the issue and evidence
- Action steps (include mention of the script)
- Closing and signature
"""

        try:
            # Get PowerShell script
            script_code = call_llm(script_prompt).strip()
            if script_code.startswith("```"):
                script_code = script_code.strip("`").split("\n", 1)[1]

            # Get email draft
            email_draft = call_llm(email_prompt).strip()

        except Exception as e:
            self.log(f"LLM call failed: {e}")
            return {
                "language": "powershell",
                "code": "Write-Output 'Script generation failed. Please check your input or retry later.'",
                "lint_passed": False,
                "email_draft": "We encountered an error while generating the script and email draft. Please try again later or refine your request."
            }

        return {
            "language": "powershell",
            "code": script_code,
            "lint_passed": any(x in script_code for x in ["$", "Remove-Item", "Clear-Content"]),
            "email_draft": email_draft
        }
