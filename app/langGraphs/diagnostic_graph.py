from langgraph.graph import StateGraph
from app.agents.diagnostic import DiagnosticAgent
# Optional: from app.agents.knowledge import KnowledgeAgent

def build_diagnostic_graph():
    diagnostic_agent = DiagnosticAgent()
    # knowledge_agent = KnowledgeAgent()

    def run_diagnostic(state):
        result = diagnostic_agent.run(state["request"])
        state["diagnosis"] = result
        return state

    def fallback_to_manual(state):
        state["diagnosis"] = {
            "root_cause": "Could not determine with high confidence.",
            "evidence": [],
            "solutions": [
                {"title": "Escalate to human support", "confidence": "low"}
            ]
        }
        return state

    def check_confidence(state):
        # Check if top solution is confident enough
        solutions = state["diagnosis"]["solutions"]
        if not solutions:
            return "fallback"
        top_confidence = solutions[0].get("confidence", "")
        return "fallback" if top_confidence not in ["high", "medium"] else "done"

    # Build subgraph
    graph = StateGraph()
    graph.add_node("diagnose", run_diagnostic)
    graph.add_node("fallback", fallback_to_manual)

    graph.add_conditional_edges("diagnose", check_confidence, {
        "done": "END",
        "fallback": "fallback"
    })

    graph.set_entry_point("diagnose")
    graph.set_finish_point("fallback")  # fallback is end if triggered

    return graph.compile()
# This graph will be used to run diagnostics and handle fallback logic
# if the confidence is not sufficient.  