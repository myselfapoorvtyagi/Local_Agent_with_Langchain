import os
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()
def get_search_tool():
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY not found in environment variables.")
        
    return TavilySearch(
        max_results=1,
        description="ONLY use this for current events, news, or generic facts not found in the local search. NEVER use this for the user's personal info."
    )