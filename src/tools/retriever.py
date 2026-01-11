import chromadb
from chromadb.utils import embedding_functions
from langchain.tools import tool

def get_retriever_tool():
    # 1. Initialize Chroma Client
    client = chromadb.PersistentClient(path="./data/chroma_db")
    
    # 2. Use the Hugging Face embedding function (miniLM)
    # This is the fastest local model for CPUs (~80MB)
    ef = embedding_functions.DefaultEmbeddingFunction()
    
    # 3. Get the collection
    collection = client.get_collection(name="local_docs", embedding_function=ef)

    # 4. Define the tool function internally so it can be wrapped
    @tool
    def search_local_knowledge(query: str) -> str:
        """
        PRIORITY TOOL: Always use this tool FIRST for questions about the user's 
        identity, resume, background, or personal documents. 
        It is much faster and more accurate for personal context than web search.
        """
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        
        # Flatten the list of documents into a single string
        if results['documents']:
            return "\n\n".join(results['documents'][0])
        return "No relevant information found in local documents."

    return search_local_knowledge