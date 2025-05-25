# schema.py

from pydantic import BaseModel, Field

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing")
    superFluous: str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    "Answer the question"
    answer: str = Field(description="250-word detailed answer to the question")
    search_queries: str = Field(
        description="1-3 search queries to improve the answer"
    )
    reflection: Reflection = Field(description="Reflection on the initial answer")
