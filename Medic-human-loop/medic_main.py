from dotenv import load_dotenv
from langchain_groq import ChatGroq
llm  = ChatGroq(model="llama-3.1-8b-instant")
from medic_graph import medic_app
from langchain_core.messages import HumanMessage
load_dotenv()



