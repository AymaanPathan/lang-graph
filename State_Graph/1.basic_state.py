from typing import TypedDict
from langgraph.graph import StateGraph,END
class SimpleState(TypedDict):
    count:int


def increment(state:SimpleState)->SimpleState:
    return {
        "count":state["count"]+1
    }


def should_increment(state):
    if(state["count"]<5):
        return "incrementNode"
    else:
        return END


# we have to give a bluprint to state graph
graph = StateGraph(SimpleState)
graph.add_node("incrementNode",increment)
graph.set_entry_point("incrementNode")
graph.add_conditional_edges("incrementNode",should_increment)

app = graph.compile()

state = {
    "count":0
}

res = app.invoke(state)
print(res)