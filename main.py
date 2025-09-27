import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.runnables.graph import MermaidDrawMethod

from nodes import run_agent_reasoning, tool_node

load_dotenv()

AGENT_REASON = "agent_reason"
ACT = "act"
LAST = -1

def should_continue(state: MessagesState) -> str:
    if not state["messages"][LAST].tool_calls:
        return END
    return ACT


flow = StateGraph(MessagesState)

flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.add_node(ACT, tool_node)
# flow.add_edge(START, AGENT_REASON) #, from_key="messages", to_key="messages")

flow.add_edge(ACT, AGENT_REASON)

flow.add_conditional_edges(AGENT_REASON, should_continue, {
    END:END,
    ACT:ACT
})

flow.set_entry_point(AGENT_REASON)


app = flow.compile()
mermaid_syntax = app.get_graph().draw_mermaid()
print(mermaid_syntax)

def main():

    res = app.invoke({"messages": [HumanMessage(content="What is the temperatur in Paris? List it and then triple it.")]})

    print(res['messages'][LAST].content)

    # In main.py, line 37
    # app.get_graph().draw_mermaid_png(output_file_path="flow.png")
    # mermaid_syntax = app.get_graph().draw_mermaid()
    # Print the syntax to your console
    # print(mermaid_syntax)


#     print("Hello ReAct langgraph with function calling!")

    # graph = app.get_graph()

    # try:
    #     graph.draw_mermaid_png(
    #         output_file_path="flow.png",
    #         draw_method=MermaidDrawMethod.PYPPETEER,
    #         max_retries=5,
    #         retry_delay=2.0,
    #     )
    #     print("Saved graph visualization to flow.png")
    # except (ImportError, PermissionError, OSError, ValueError) as err:
    #     print(
    #         "Could not render PNG with Pyppeteer (", err, ") — writing Mermaid markup instead.",
    #         sep="",
    #     )
    #     mermaid_path = "flow.mmd"
    #     with open(mermaid_path, "w", encoding="utf-8") as mermaid_file:
    #         mermaid_file.write(graph.draw_mermaid())
    #     print("Saved Mermaid definition to", mermaid_path)


if __name__ == "__main__":
    main()
    # asyncio.run(main())
    # pass