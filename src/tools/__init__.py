from .search import get_search_tool
from .retriever import get_retriever_tool
from .calculator import calculator_tool # Import here

search_tool = get_search_tool()
retriever_tool = get_retriever_tool()

# Add to the list
all_tools = [search_tool, retriever_tool, calculator_tool]