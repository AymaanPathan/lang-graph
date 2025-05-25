# execute_tool.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from dotenv import load_dotenv
import json
import datetime
from schema import AnswerQuestion

load_dotenv()

# Setup
llm = ChatOllama(model="mistral")
search_tool = TavilySearchResults()

def getCurrentTime():
    return datetime.datetime.now().isoformat()

# --- Prompt Template ---
actor_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            """You are an AI Researcher. Current Time: {time}
1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After reflection, **list 1-3 search queries separately** for researching improvements."""
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "You must return the answer strictly as a tool call using this format:\n\n"
            "{{\"tool_calls\": [{{\"tool_name\": \"AnswerQuestion\", \"tool_input\": {{\"answer\": \"<your answer>\"}}}}]}}"
        )
    ]
).partial(time=getCurrentTime)

# First response prompt
first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed 250-word answer"
)

# Revise instructions
revise_instruction = """Revise your previous answer using the new information.
- Use the previous critique to add missing info and remove superfluous parts.
- Must not exceed 250 words.
- Include numerical citations like [1], [2], etc.
- Add a "References" section:
  - [1] https://example.com
  - [2] https://example.com"""

revisior_prompt_template = actor_prompt_template.partial(
    first_instruction=revise_instruction
)

# Chains
first_responder_chain = first_responder_prompt_template | llm.with_structured_output(AnswerQuestion)
revisior_chain = revisior_prompt_template | llm.with_structured_output(AnswerQuestion)


# Execution of web search
def run_pipeline(user_question: str):
    # Step 1: Initial Answer
    first_response = first_responder_chain.invoke({
        "messages": [HumanMessage(content=user_question)]
    })

    print("\n=== Initial Answer ===")
    print(first_response.answer)
    print("\n=== Reflection ===")
    print("Missing:", first_response.reflection.missing)
    print("Superfluous:", first_response.reflection.superFluous)
    print("\n=== Suggested Queries ===")
    print(first_response.search_queries)

    # Step 2: Tavily Search (dynamic, safe)
    queries = [
        q.strip()
        for q in first_response.search_queries.strip().split("\n")
        if q.strip()
    ]

    references = []
    for query in queries:
        results = search_tool.invoke({"query": query})
        print(f"\nResults for query '{query}': {results}")

        if results and isinstance(results, list):
            top_result = results[0]
            if isinstance(top_result, dict) and "url" in top_result:
                references.append(top_result["url"])
        else:
            print("Top result does not contain 'url':", top_result)
    else:
        print("Unexpected results format or empty:", results)


    reference_text = "\n".join([f"[{i+1}] {url}" for i, url in enumerate(references)])

    # Step 3: Revised Answer
    revised_input = {
        "messages": [
            HumanMessage(content=(
                f"{first_response.answer}\n\n"
                f"Reflection:\nMissing: {first_response.reflection.missing}\n"
                f"Superfluous: {first_response.reflection.superFluous}\n\n"
                f"References:\n{reference_text}"
            ))
        ]
    }

    revised_response = revisior_chain.invoke(revised_input)

    print("\n=== Revised Answer ===")
    print(revised_response.answer)
    print("\n=== References ===")
    for i, url in enumerate(references, start=1):
        print(f"[{i}] {url}")


if __name__ == "__main__":
    question = "write a blog on how perplexity Ai was build"
    run_pipeline(question)
