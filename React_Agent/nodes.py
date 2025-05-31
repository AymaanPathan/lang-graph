from dotenv import load_dotenv
from langgraph.prebuilt.chat_agent_executor import create_tool_calling_executor
from agent_reason_runnable import  react_agent_runnable,tools
from react_state import AgentState
import ast


load_dotenv()

# Node 1
def invokeAgentState(state:AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome":agent_outcome}


# Node 2
def act_node(state: AgentState):
    agent_action = state["agent_outcome"]
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input

    if isinstance(tool_input, str):
        if (tool_input.startswith('(') and tool_input.endswith(')')) or \
           (tool_input.startswith('{') and tool_input.endswith('}')):
            try:
                tool_input = ast.literal_eval(tool_input)
            except Exception as e:
                print(f"Failed to parse tool_input with literal_eval: {tool_input}, error: {e}")

    tool_function = next((tool for tool in tools if tool.name == tool_name), None)

    if tool_function:
        if isinstance(tool_input, dict):
            output = tool_function.invoke(**tool_input)
        else:
            output = tool_function.invoke(tool_input)
    else:
        output = f"Tool {tool_name} Not Found"

    return {"intermediate_steps": [(agent_action, str(output))]}


