from dotenv import load_dotenv
from langgraph.graph import StateGraph,END
from Chat_State import BasicChatMessages 
from chat_with_tool import llm_with_tools
from langgraph.prebuilt import ToolNode
from chat_with_tool import tools
from langchain_core.messages import HumanMessage
# Start the chat

load_dotenv()
def chatBot(state:BasicChatMessages):
    return {
        "messages":[llm_with_tools.invoke(state["messages"])]
    }

# Check if message has tool call or not
def check_tool(state:BasicChatMessages):
    # Last because in the end we get a message from ai that is last 
    last_message = state["messages"][-1]

    if(hasattr(last_message,"tool_calls")and len(last_message.tool_calls)>0):
        return "tool_node"
    else:
        return END


tool_node = ToolNode(tools=tools)
graph = StateGraph(BasicChatMessages)
graph.add_node("chatbot",chatBot)
graph.add_node("tool_node",tool_node)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot",check_tool)
# tool_node will always go to chatbot because tool_node does not give final answer  
graph.add_edge("tool_node","chatbot")

app = graph.compile()

while True:
    userInput = input("Ask The Ai:")
    if userInput=="Exit" or userInput=="exit":
        break 
    else:
        result = app.invoke({
            "messages":[HumanMessage(content=userInput)]
        })
        print(result)
