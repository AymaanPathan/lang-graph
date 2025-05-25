from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import MessageGraph,END
from chains import generation_chain,reflection_chain
load_dotenv()

graph = MessageGraph() #creates a empty graph

# Names of nodes
GENERATE = "generate"
REFLECT = "reflect"

# Create a node of graph

def generateNode(state): #state is basically the message of previous node
   return generation_chain.invoke({
        "messages":state
    })


def reflectNode(state): #state is basically the message of previous node
   response =  reflection_chain.invoke({
        "messages":state
    })
   return HumanMessage(content=response.content)
   

graph.add_node(GENERATE,generateNode)
graph.add_node(REFLECT,reflectNode)
graph.set_entry_point(GENERATE)

def shouldContinue(state):
    if len(state) > 2:
        return END
    return REFLECT



graph.add_conditional_edges(GENERATE,shouldContinue)  # after generate we add condition
graph.add_edge(REFLECT,GENERATE) # after    reflect always go to generate




app = graph.compile()
initial_state = [HumanMessage(role="user", content="i have felling tired without doing anything")]
output = app.invoke(initial_state)
print("Final Output:\n", output)