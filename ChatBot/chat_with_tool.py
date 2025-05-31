from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq

search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

llm = ChatGroq(model="llama-3.1-8b-instant")
llm_with_tools = llm.bind_tools(tools=tools)