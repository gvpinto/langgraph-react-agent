from dotenv import load_dotenv

load_dotenv()
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

try:
    from langchain_tavily import TavilySearch  # type: ignore
except ImportError:  # tavily is optional; skip if not installed
    TavilySearch = None


@tool
def triple(num: float) -> float:
    """
    Triples a number.
    args:
        num: number to be tripled
    returns:
        tripled number
    """
    return num * 3


tools = [TavilySearch(max_results=1), triple] # if TavilySearch is not None else [triple]

# tools = []

# if TavilySearch is not None:
#     tools.append(TavilySearch(max_results=1))
# else:
#     print("Warning: langchain_tavily not installed; continuing without TavilySearch tool.")

# tools.append(triple)


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)
