from typing import TypedDict
from langgraph.graph import StateGraph,END

class NumberState(TypedDict):
    number:int
    log:list[str]


def increment(state:NumberState)->NumberState:
    return {
        "number":state["number"]+1,
        "log":state["log"]
    }

def checkIsEven(state):
    if(state["number"]%2==0):
        state["log"].append(f"Even number reached: {state['number']}")

    if(state["number"]>=10):
            return END
    return "IncrementNode",


graph = StateGraph(NumberState)
graph.add_node("IncrementNode",increment)
graph.set_entry_point("IncrementNode")
graph.add_conditional_edges("IncrementNode",checkIsEven)

app = graph.compile()
state = {
    "number":1,
    "log":[]
}
res =app.invoke(state)
print(res)
