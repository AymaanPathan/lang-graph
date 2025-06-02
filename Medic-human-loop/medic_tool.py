from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain.agents import create_react_agent
from medic_main import llm
from langchain import hub

load_dotenv()

search_tool = TavilySearchResults()

tools= [search_tool]

react_prompt = hub("hwchase17/react")

llm_with_tool = create_react_agent(llm=llm,tools=tools,prompt=react_prompt)