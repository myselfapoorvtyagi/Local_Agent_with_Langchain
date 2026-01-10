import os
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()
def get_search_tool():
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY not found in environment variables.")
        
    return TavilySearch(
        max_results=3,
        description="A search engine optimized for comprehensive, accurate, and real-time results from the web."
    )