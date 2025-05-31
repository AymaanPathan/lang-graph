from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph import app
load_dotenv()


while True:
    userInput = input("Ask The Ai:")
    if userInput=="Exit" or userInput=="exit":
        break 
    else:
        result = app.invoke({
            "messages":[HumanMessage(content=userInput)]
        })
        print(result)
