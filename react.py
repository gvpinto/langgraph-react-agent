from dotenv import load_dotenv

load_dotenv()
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_tavily import TavilySearch


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


tools = [TavilySearch(max_results=1), triple]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)
