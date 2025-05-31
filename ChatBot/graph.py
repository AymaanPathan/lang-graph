from dotenv import load_dotenv
from langgraph.graph import StateGraph,END
from Chat_State import BasicChatMessages
from langchain_groq import ChatGroq
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)


def chatBot(state:BasicChatMessages):
    return {
        "messages":[llm.invoke(state["messages"])]
    }


graph =StateGraph(BasicChatMessages)
graph.add_node("chat",chatBot)
graph.set_entry_point("chat")
graph.add_edge("chat",END)
app =graph.compile()

