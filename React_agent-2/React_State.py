from langchain_core.agents import AgentAction,AgentFinish
from typing import TypedDict,Union,Annotated
import operator

class Agent_State(TypedDict):
    input:str
    agent_outcome:Union[AgentAction,AgentFinish,None] # it can be None so dont throw error
    Next_action:Annotated[list[tuple[AgentAction,str]],operator.add]  #adding list of agent action