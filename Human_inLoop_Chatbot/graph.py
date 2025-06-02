from dotenv import load_dotenv
from langgraph.graph import StateGraph,END
from Human_loop_Chat_state import MessageState
from langchain_core.messages import HumanMessage
from main import llm
load_dotenv()

# Nodes Name
GENERATE_POST = "GENERATE_POST"
GET_REVIEW = "GET_REVIEW"
POST_TO_LINKEDIN = "POST_TO_LINKEDIN" 
COLLECT_FEEDBACK = "COLLECT_FEEDBACK"



# Generate Post
def generate_post(state:MessageState):
    return {
        "messages":[llm.invoke(state["messages"])]
    }

# Get Review Of post
def get_Review(state:MessageState):
    last_msg = state["messages"][-1].content
    print("\n Current Linkedin Post")
    print(last_msg)
    ask_to_post = input("Post to Linkedin (Yes/No)")
    if(ask_to_post=="Yes" or ask_to_post=="yes"):
        return POST_TO_LINKEDIN
    else:
        return COLLECT_FEEDBACK
    
# Collect_FeedBack
def collect_feedback():
    userFeedBack = input("How Can I Improve This Post :")
    return {
        "messages":[HumanMessage(content=userFeedBack)]
    }


# POST_TO_LINKEDIN
def post_to_linkedin(state:MessageState):
    last_msg = state["messages"][-1].content
    print("\n Final Linkedin Post")
    print(last_msg)
    print("\n Post been Approved Posted To Linked🟢")
    
    
    
# Post The output
graph = StateGraph(MessageState)
graph.add_node(GENERATE_POST,generate_post)
graph.add_node(GET_REVIEW,get_Review)
graph.add_node(COLLECT_FEEDBACK,collect_feedback)
graph.add_node(POST_TO_LINKEDIN,post_to_linkedin)

# Edges
graph.set_entry_point(GENERATE_POST)
graph.add_conditional_edges(GENERATE_POST,get_Review)
graph.add_edge(POST_TO_LINKEDIN,END) # after post its end the graph
graph.add_edge(COLLECT_FEEDBACK,GENERATE_POST) # after collecting info generate will run everytime

user_question = "Create a Linkedin Post About ai agent taking over human job"

app = graph.compile()
response =app.invoke({
    "messages":HumanMessage(content=user_question),
})
print(response)