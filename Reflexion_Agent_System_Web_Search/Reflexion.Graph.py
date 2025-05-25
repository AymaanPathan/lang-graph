from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import MessageGraph,END
from chain import first_responder_chain,revisior_chain
graph = MessageGraph()

graph.add_node("First_Draft")