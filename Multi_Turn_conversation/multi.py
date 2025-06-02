from langgraph.graph import StateGraph,END,START
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from Message_State import Message_State
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langgraph.types import Command,interrupt
import uuid

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

def model_generating_linkedin_post(state:Message_State):
    """here we are using llm to generate linkedin post
    with human suggestions
    """
    print("[model] generating...")
    linkedin_topic = state["linkedin_topic"]
    feedBack=[] 
    if "human_feedBack" in state:
        feedBack = state["human_feedBack"]
    else:
        feedBack = ["No Feedback from user"]

    prompt = f"""
    Linkedin_topic : {linkedin_topic}
    Human Feedback :{feedBack[-1] if feedBack else "No Feedback"}
    Generating a well Structured In Markdown Format including bullet points
    based on given topic
    Consider Previous Human Feedback to refine the response
    """   
    response = llm.invoke([
        SystemMessage(content="You Are a Expert linkedin Content Creator "),
        HumanMessage(content=prompt)
    ])
    generated_linkedin_post = response.content
    print("Ai Generated Post : ",generated_linkedin_post)
    return {
        "linkedin_topic":linkedin_topic,
        "generated_post":generated_linkedin_post,
        "human_feedBack":feedBack
    }


def human_interrupting(state:Message_State):
    "Human intervention Node Where We will loop until user says to stop"
    print("Awaiting for feedback...")
    generated_post = state["generated_post"]

    user_feedBack = interrupt(
        {
        "generated_post":generated_post,
        "message":"Provide feedback or type 'done' to Finish"
        }
    )
    print(f"[Human node] received human feedback :{user_feedBack}")
    if(user_feedBack.lower()=="done"):
        return Command(update={"human_feedBack":state["human_feedBack"]+["Finialised"]},goto="end_node")
    
    return Command(update={"human_feedBack":state["human_feedBack"]+[user_feedBack]},goto="model") 


def end_node(state:Message_State):
    """Final Node"""
    print("\n[end_node] Process Finished")
    print("\n Final Post" , state["generated_post"][-1])
    print("\n Final Human Feed Back" , state["human_feedBack"])
    return {
        "generated_post":state["generated_post"],
        "human_feedBack":state["human_feedBack"]
    }



graph = StateGraph(Message_State)
graph.add_node("model",model_generating_linkedin_post)
graph.add_node("human_node",human_interrupting)
graph.add_node("end_node",end_node)

# Flow
graph.set_entry_point("model")
graph.add_edge(START,"model")
graph.add_edge("model","human_node")
graph.set_finish_point("end_node")


checkPointer = MemorySaver()
app = graph.compile(checkpointer=checkPointer)
thread_config = {
    "configurable": {
        "thread_id": str(uuid.uuid4())
    }
}


Linkedin_topic = input("Enter Topic : ")
initial_state ={
    "linkedin_topic":Linkedin_topic,
    "generated_post":[],
    "human_feedBack":[]
}

for chunk in app.stream(initial_state, config=thread_config):
    for node_id, value in chunk.items():
        if node_id == "__interrupt__":
            while True:
                user_feedback = input("Provide Feedback or type (done) to Finish: ")
                app.invoke(Command(resume=user_feedback), config=thread_config)
                if user_feedback.lower() == "done":
                    break
