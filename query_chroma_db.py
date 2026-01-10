import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def inspect_chroma():
    # 1. Connect to the existing DB
    # Ensure the path and collection_name match your ingest.py
    persist_directory = "./data/chroma_db"
    collection_name = "local_docs"
    
    embeddings = OllamaEmbeddings(model="llama3")
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=collection_name
    )

    # 2. Get stats
    # Access the underlying Chroma client collection
    collection = vectorstore._collection
    count = collection.count()
    
    print(f"--- 📊 ChromaDB Stats ---")
    print(f"Total Chunks in '{collection_name}': {count}")
    
    if count == 0:
        print("⚠️ The database is empty. Did you run ingest.py?")
        return

    # 3. Peek at the data (Raw Query)
    print(f"\n--- 📄 Previewing first 3 chunks ---")
    results = collection.get(limit=3, include=["documents", "metadatas"])
    
    for i in range(len(results["ids"])):
        print(f"\n[ID: {results['ids'][i]}]")
        print(f"[Source: {results['metadatas'][i].get('source', 'Unknown')}]")
        print(f"Content Snippet: {results['documents'][i][:200]}...")
        print("-" * 30)

if __name__ == "__main__":
    inspect_chroma()