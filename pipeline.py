from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)

def run_research_pipeline(topic: str):

    state = {}

    print("\n" + "+" * 50)
    print("STEP 1 - SEARCH AGENT")
    print("+" * 50)

    search_agent = build_search_agent()

    search_results = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent and reliable information about: {topic}"
            )
        ]
    })

    state["search_results"] = search_results["messages"][-1].content

    print(state["search_results"])

    print("\n" + "+" * 50)
    print("STEP 2 - READER AGENT")
    print("+" * 50)

    reader_agent = build_reader_agent()

    reader_results = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
From these search results:

{state['search_results']}

Choose the most useful URL.
Scrape it and summarize the content.
"""
            )
        ]
    })

    state["scraped_content"] = reader_results["messages"][-1].content

    print(state["scraped_content"])

    print("\n" + "+" * 50)
    print("STEP 3 - WRITER")
    print("+" * 50)

    combined_research = f"""
Search Results:
{state['search_results']}

Scraped Content:
{state['scraped_content']}
"""

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": combined_research
    })

    print("\nFINAL REPORT\n")
    print(state["report"])

    print("\n" + "+" * 50)
    print("STEP 4 - CRITIC")
    print("+" * 50)

    state["critique"] = critic_chain.invoke({
        "report": state["report"]
    })

    print(state["critique"])

    return state


if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_research_pipeline(topic)