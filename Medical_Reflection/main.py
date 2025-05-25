from chains import first_chain,revised_chain
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults

search_tool = TavilySearchResults()


def run_pipeline(user_question: str):
    # Step 1: Initial Answer
    first_response = first_chain.invoke({
        "messages": [HumanMessage(content=user_question)]
    })

    print("\n=== Initial Answer ===")
    print(first_response.Answer)
    print("\n=== Reflection ===")
    print("Missing:", first_response.reflection.missing)
    print("Superfluous:", first_response.reflection.superfluous)
    print("\n=== Suggested Queries ===")
    print(first_response.web_search)

    # Step 2: Tavily Search (dynamic, safe)
    queries = []
    # Correct way to loop through list of strings
    for q in first_response.web_search:
        queries.append(q.strip())


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
                f"{first_response.Answer}\n\n"
                f"Reflection:\nMissing: {first_response.reflection.missing}\n"
                f"Superfluous: {first_response.reflection.superfluous}\n\n"
                f"References:\n{reference_text}"
            ))
        ]
    }

    revised_response = revised_chain.invoke(revised_input)

    print("\n=== Revised Answer ===")
    print(revised_response.Answer)
    print("\n=== References ===")
    for i, url in enumerate(references, start=1):
        print(f"[{i}] {url}")


if __name__=="__main__":
    question = "i have a little pain on my chest when i breathe"
    run_pipeline(question)