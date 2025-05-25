from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

generation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a Twitter techie influencer assistant tasked with writing excellent Twitter posts. "
        "Generate the best Twitter post possible for the user's request. "
        "If the user provides critique, respond with a revised version of your previous post."
    ),
    MessagesPlaceholder(variable_name="messages") # append new message on runtime
])

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. generate critique and"
            "recommendations for the user's tweet"
            "always provide detailed recommendations , including requests for length"
            "virality , style etc.."
        ),
    MessagesPlaceholder(variable_name="messages") # append new message on runtime
    ]
)

llm = ChatOllama(model="mistral")
generation_chain = generation_prompt |llm
reflection_chain = reflection_prompt |llm