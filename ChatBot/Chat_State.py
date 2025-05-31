from typing import TypedDict,Annotated,List
from langgraph.graph import add_messages

class BasicChatMessages(TypedDict):
    messages:Annotated[List,add_messages]