from langgraph.graph import StateGraph,END
from medic_state import medic_chat_bot_state
from medic_state import medic_chat_bot_state
from medic_main import llm
from langchain_core.messages import HumanMessage
# nodes
GENERATE_GENERIC_SOLUTION="GENERATE_GENERIC_SOLUTION"
COLLECTS_MORE_SYMPTOMS="COLLECTS_MORE_SYMPTOMS"
GENERATE_ACCURATE_SOLUTION_WITH_MORE_SYMPTOMS = "GENERATE_ACCURATE_SOLUTION_WITH_MORE_SYMPTOMS"

def generate_solution_for_disease(state:medic_chat_bot_state):
    return {
        "messages":[llm.invoke(state["messages"])]
    }

def collects_more_user_symptoms(state:medic_chat_bot_state):
    last_msg = state["messages"][-1].content
    print("\n current Solution")
    print(last_msg)
    user_input = input("Any More Symptoms (Yes/No) : ")
    if(user_input=="yes"):
        return GENERATE_ACCURATE_SOLUTION_WITH_MORE_SYMPTOMS
    else:
        return END

def generate_accurate(state: medic_chat_bot_state):
    user_input = input("Provide More Info About Your disease: ")
    return {
        "messages": state["messages"] + [HumanMessage(content=user_input)]
    }

graph = StateGraph(medic_chat_bot_state)
graph.add_node(GENERATE_GENERIC_SOLUTION,generate_solution_for_disease)
graph.add_node(COLLECTS_MORE_SYMPTOMS,collects_more_user_symptoms)
graph.add_node(GENERATE_ACCURATE_SOLUTION_WITH_MORE_SYMPTOMS,generate_accurate)

# Edgnes
graph.set_entry_point(GENERATE_GENERIC_SOLUTION)
graph.add_conditional_edges(GENERATE_GENERIC_SOLUTION,collects_more_user_symptoms)
graph.add_edge(COLLECTS_MORE_SYMPTOMS,END)

medic_app = graph.compile()


while True:
    user_prompt = input("Ask Ai About Your Problem :")
    if(user_prompt=="exit" or user_prompt=="Exit"):
        break
    else:
        response = medic_app.invoke({
            "messages":HumanMessage(content=user_prompt)
        })
        print(response)