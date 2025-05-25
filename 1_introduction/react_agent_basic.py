from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain.agents import initialize_agent,tool
from langchain_community.tools import TavilySearchResults
import datetime

load_dotenv()
llm = ChatOllama(
    model="mistral"
)

@tool
def currentTime(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Returns the current date and time. Input should be a format string like "%Y-%m-%d %H:%M:%S"."""
    return datetime.datetime.now().strftime(format)




search_tool = TavilySearchResults(search_depth="basic")
tools = [search_tool,currentTime]

agent =initialize_agent(
    tools=tools,llm=llm,agent="zero-shot-react-description",
    verbose=True,    
    handle_parsing_errors=True)
agent.invoke("Get the current time in the format %Y-%m-%d %H:%M:%S and ")