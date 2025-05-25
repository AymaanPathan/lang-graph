from langchain_ollama import ChatOllama
from pydantic import BaseModel,Field

llm = ChatOllama(model="mistral")

class MedInfo(BaseModel):
    """information about medicine"""
    name:str = Field(description="name of the medicine")
    description:str = Field(description="description of the medicine")
    risk:str = Field(description="risk of the medicine")


structured_llm = llm.with_structured_output(MedInfo)
res  = structured_llm.invoke("what is dolo medicine")
print(res)