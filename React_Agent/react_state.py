import operator
from typing import Annotated,TypedDict,Union
from langchain_core.agents import AgentAction,AgentFinish

class AgentState(TypedDict):
    input:str
    agent_outcome:Union[AgentAction,AgentFinish,None] # it can be None so dont throw error
    intermediate_steps:Annotated[list[tuple[AgentAction,str]],operator.add]  #adding list of agent action 