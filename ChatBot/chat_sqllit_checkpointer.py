from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,END
from Chat_State import BasicChatMessages
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

sqlite_Connection = sqlite3.connect("checkpoint.sqlite",check_same_thread=False)
load_dotenv()

memory = SqliteSaver(sqlite_Connection)

llm  = ChatGroq(model="llama-3.1-8b-instant")

def chatBot(state:BasicChatMessages):
    return {
        "messages":[llm.invoke(state["messages"])]
    }

graph = StateGraph(BasicChatMessages)
graph.add_node("chat",chatBot)
graph.set_entry_point("chat")
graph.add_edge("chat",END)
app = graph.compile(checkpointer=memory)

config = {"configurable":{
    "thread_id":1
}}

while True:
    userQuestion = input("Ask AI: ")
    if userQuestion=="Exit" or userQuestion=="exit":
        break
    else:
        result = app.invoke({
            "messages":HumanMessage(content=userQuestion)
        },config=config)
        print("AI : " + result["messages"][-1].content)

