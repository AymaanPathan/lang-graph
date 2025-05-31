from dotenv import load_dotenv
from langgraph.graph import StateGraph,END
from Human_loop_Chat_state import MessageState
from main import llm

# Nodes Name
GENERATE_POST = "GENERATE_POST"
POST_TO_LINKEDIN = "POST_TO_LINKEDIN" 
COLLECT_FEEDBACK = "COLLECT_FEEDBACK"



# Generate Post
def generate_post(state:MessageState):
    return {
        "messages":[llm.invoke(state["messages"])]
    }

# Get Review Of post
def review_post(state:MessageState):
    last_msg = state["messages"][-1].content
    print("\n Current Linkedin Post")
    print(last_msg)
    ask_to_post = input("Post to Linkedin (Yes/No)")
    if(ask_to_post=="Yes"):
        return POST_TO_LINKEDIN
    else:
        return COLLECT_FEEDBACK
    
# POST_TO_LINKEDIN
def post_to_linkedin(state:MessageState):
    last_msg = state["messages"][-1].content
    print("\n Current Linkedin Post")
    print(last_msg)
    user_input = input("Want To Post To Linkedin")
    
    
# Post The output
graph = StateGraph(MessageState)
graph.add_node(GENERATE_POST,generate_post)
graph.add_node(POST_TO_LINKEDIN)