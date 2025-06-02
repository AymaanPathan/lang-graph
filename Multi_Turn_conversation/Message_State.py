from typing import TypedDict,Annotated,List
from langgraph.graph import StateGraph,add_messages

class Message_State(TypedDict):
    linkedin_topic:str
    generated_post:Annotated[List[str],add_messages]
    human_feedBack:Annotated[List[str],add_messages]