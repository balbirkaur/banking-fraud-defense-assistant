from langgraph.graph import StateGraph, END

# Define simple state
class State(dict):
    text: str

# Node function
def hello_node(state):
    return {"text": state["text"] + " — processed successfully"}

# Build graph
graph = StateGraph(State)
graph.add_node("hello", hello_node)
graph.set_entry_point("hello")
graph.add_edge("hello", END)

app = graph.compile()

# Run
result = app.invoke({"text": "LangGraph setup verified"})
print(result)
