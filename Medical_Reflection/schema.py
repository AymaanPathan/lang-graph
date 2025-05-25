from pydantic import BaseModel,Field
from typing import List

class Reflection(BaseModel):
    missing: str = Field(
        ...,
        description="Details about missing or incomplete information in the initial AI response."
    )
    superfluous: str = Field(
        ...,
        description="Details about unnecessary or irrelevant parts of the initial AI response."
    )

class MedicAnswer(BaseModel):
    Answer:str =Field(description=(
            "Answer contains bullet points categorizing risk factors "
            "into High, Moderate, and Low based on the user's medical question. "
            "For example, if the question is 'I have a sore throat', "
            "the answer will list remedies or advice grouped by these risk levels."
        ))
    web_search: List[str] = Field(
    default_factory=list,
    description="List of URLs or references retrieved from web search related to the answer."
    )
    reflection :Reflection = Field(description="Reflection on the initial answer")