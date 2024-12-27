from langgraph.graph import (
    StateGraph,
    END
)
from nodes.nodes import (
    generate_context, 
    generate_summary,
    generate_analysis,
    suggest_actions
)
from schemas.schemas import GraphState

workflow = StateGraph(GraphState)

workflow.add_node("generate_context", generate_context)
workflow.add_node("generate_summary", generate_summary)
workflow.add_node("generate_analysis", generate_analysis)
workflow.add_node("suggest_actions", suggest_actions)

workflow.set_entry_point("generate_context")
workflow.add_edge('generate_context', "generate_summary")
workflow.add_edge('generate_summary', "generate_analysis")
workflow.add_edge('generate_analysis', "suggest_actions")
workflow.add_edge('suggest_actions', END)

app = workflow.compile()