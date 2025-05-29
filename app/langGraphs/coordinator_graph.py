from langgraph.graph import StateGraph, END
from app.langGraphs.diagnostic_graph import build_diagnostic_graph
from app.agents.automation import AutomationAgent
from app.agents.writer import WriterAgent

def build_coordinator_graph():
    # Agents
    automation_agent = AutomationAgent()
    writer_agent = WriterAgent()

    # 1️⃣ Load pre-built diagnostic subgraph
    diagnostic_subgraph = build_diagnostic_graph()

    # 2️⃣ Diagnostic node (calls the diagnostic subgraph)
    def run_diagnostic(state):
        # The diagnostic_subgraph should be invoked using its .invoke() method
        return diagnostic_subgraph.invoke(state)

    # 3️⃣ Script node
    def run_automation(state):
        result = automation_agent.run(state["request"])
        state["script"] = result
        return state

    # 4️⃣ Writer node
    def run_writer(state):
        result = writer_agent.run({
            "root_cause": state["diagnosis"]["root_cause"],
            "evidence": state["diagnosis"]["evidence"],
            "script": state["script"]["code"]
        })
        state["email_draft"] = result["content"]
        return state

    # 🧠 Build full coordinator graph
    graph = StateGraph()

    graph.add_node("diagnose", run_diagnostic)
    graph.add_node("generate_script", run_automation)
    graph.add_node("write_summary", run_writer)

    graph.set_entry_point("diagnose")
    graph.add_edge("diagnose", "generate_script")
    graph.add_edge("generate_script", "write_summary")
    graph.set_finish_point("write_summary")

    return graph.compile()