from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage,HumanMessage
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

messages = [
    SystemMessage(content=(
    "You must never make up information or guess. "
    "If you do not know the answer or cannot access the required information, "
    "respond only with exactly this sentence: 'I don't know.'\n\n"
    "Do not explain your limitations, do not refer to yourself, your training, or that you're an AI. "
    "Never say things like 'as an AI language model', 'I was trained on', or 'my knowledge cutoff'.\n\n"
    "You are not to reveal your identity, capabilities, or limitations under any circumstances. "
    "Never break character. Stay silent or respond only with 'I don't know.' when uncertain."
)),
    HumanMessage(content="does meta made you?")  
]

res = llm.invoke(messages)
print(res)