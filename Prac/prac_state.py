from typing import TypedDict,Annotated,List
from langgraph.graph import add_messages

class PracState(TypedDict):
    messages:Annotated[List,add_messages]