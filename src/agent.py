import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from .state import AgentState
from .llm import get_model
from .tools import all_tools

def build_agent():
    workflow = StateGraph(AgentState)
    llm = get_model().bind_tools(all_tools)

    # Define Nodes
    def call_brain(state):
        return {"messages": [llm.invoke(state["messages"])]}

    from langgraph.prebuilt import ToolNode
    tool_node = ToolNode(all_tools)

    workflow.add_node("brain", call_brain)
    workflow.add_node("action", tool_node)

    workflow.set_entry_point("brain")
    workflow.add_conditional_edges(
        "brain",
        lambda x: "action" if x["messages"][-1].tool_calls else "end",
        {"action": "action", "end": END}
    )
    workflow.add_edge("action", "brain")

    # FIX: SqliteSaver must be used as a context manager
    # We return the workflow, and compile it in main.py or a wrapper
    return workflow