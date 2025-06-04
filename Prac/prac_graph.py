from langgraph.graph import StateGraph,END
from prac_state import PracState
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode
from main_prac import llm
from langchain_core.messages import SystemMessage 
from langgraph.types import Command
from langchain_community.tools import TavilySearchResults

search_tool = TavilySearchResults()
tools= [search_tool]

# Chat Node 
def chat_node(state:PracState):
    result = llm.invoke(state["messages"])
    return {
        "messages":[result]
    }
    



# Tool_Router_Node 
def tool_router(state:PracState):
    last_message = state["messages"][-1].content
    if last_message == "I don't know.":
        user_input = input("LLM Doesn't Know. Should It Try Web Search? (yes/no): ")
        if user_input.lower() == "yes":
            return Command(goto="tool_node", update={})  # ✅ Use Command instead of string
    return Command(goto="chat", update={})

tool_node = ToolNode(tools=tools)



graph = StateGraph(PracState)
graph.add_node("chat",chat_node)
graph.add_node("tool_router",tool_router)
graph.add_node("tool_node",tool_node)

# Flow
graph.set_entry_point("chat")
graph.add_edge("chat", "tool_router")
graph.add_edge("tool_router","tool_node")
graph.add_edge("tool_router","chat")
graph.add_edge("tool_node", END)

app = graph.compile()

messages = [
    SystemMessage(content=(
    "You must never make up information or guess. "
    "If you do not know the answer or cannot access the required information, "
    "respond only with exactly this sentence: 'I don't know.'\n\n"
    "Do not explain your limitations, do not refer to yourself, your training, or that you're an AI. "
    "Never say things like 'as an AI language model', 'I was trained on', or 'my knowledge cutoff'.\n\n"
    "You are not to reveal your identity, capabilities, or limitations under any circumstances. "
    "Never break character. Stay silent or respond only with 'I don't know.' when uncertain."
)),
    HumanMessage(content="current weather on pune?")
]

res = app.invoke({
     "messages": messages
})
print(res)