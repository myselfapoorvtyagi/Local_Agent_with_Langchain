import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def ingest_docs():
    # 1. Load and Split (Keep using LangChain for this, as it's great at PDF handling)
    loader = DirectoryLoader('./docs', glob="./*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # Extract just the text and metadata for Chroma's native .add()
    content = [doc.page_content for doc in splits]
    metadata = [doc.metadata for doc in splits]
    ids = [f"id_{i}" for i in range(len(splits))]

    # 2. Set up native Chroma Client
    # This replaces the LangChain "Chroma.from_documents" call
    client = chromadb.PersistentClient(path="./data/chroma_db")
    
    # 3. Choose your Embedding Function
    # Option A: Using the model you wanted (requires sentence-transformers)
    # ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Option B: The "Safe" Default (Uses ONNX, often avoids the import error)
    ef = embedding_functions.DefaultEmbeddingFunction()

    # 4. Create Collection and Add Data
    collection = client.get_or_create_collection(
        name="local_docs", 
        embedding_function=ef
    )
    
    collection.add(
        documents=content,
        metadatas=metadata,
        ids=ids
    )
    
    print(f"✅ Successfully ingested {len(splits)} chunks using Native Chroma utils!")

if __name__ == "__main__":
    ingest_docs()