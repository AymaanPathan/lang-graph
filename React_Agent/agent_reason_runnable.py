from langchain.agents import create_react_agent, tool
from dotenv import load_dotenv
import datetime
from langchain_ollama import ChatOllama
from langchain_community.tools import TavilySearchResults
from langchain import hub
import os

# Load environment
load_dotenv(dotenv_path="D:/Lang-Graph/.env")

# Define LLM
llm = ChatOllama(model="mistral")

# Define tools
search_tool = TavilySearchResults(search_depth="basic")

@tool
def get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Returns the current date and time. Input should be a format string like '%Y-%m-%d %H:%M:%S'."""
    return datetime.datetime.now().strftime(format)


# Pull prompt
react_prompt = hub.pull("hwchase17/react")

# Create agent with tools
tools = [search_tool, get_current_time]  # <-- Use the assigned tool function here

react_agent_runnable = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=react_prompt
)
