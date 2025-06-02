from typing import TypedDict,Annotated,List
from langgraph.graph import add_messages

class medic_chat_bot_state(TypedDict):
    messages:Annotated[List,add_messages]