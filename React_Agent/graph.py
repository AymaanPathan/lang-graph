from dotenv import load_dotenv
from react_state import AgentState
from nodes import invokeAgentState ,act_node
from langchain_core.agents import AgentAction,AgentFinish
from langgraph.graph import StateGraph,END

REASON_NODE ="reason_node"
ACT_NODE= "act_node"
env = load_dotenv(dotenv_path="D:/Lang-Graph/.env")
print(env)


def shouldContinue(state:AgentState)->str:
    if(isinstance(state["agent_outcome"],AgentFinish)):
        return END
    
    return ACT_NODE


graph =StateGraph(AgentState)
graph.add_node(REASON_NODE,invokeAgentState)
graph.set_entry_point(REASON_NODE)
graph.add_node(ACT_NODE,act_node)
graph.add_conditional_edges(REASON_NODE,shouldContinue)

app = graph.compile()
result = app.invoke({
    "input":"How many days ago was the latest spaceX launch",
    "agent_outcome":None,
    "intermediate_steps":[]
})
print(result)
