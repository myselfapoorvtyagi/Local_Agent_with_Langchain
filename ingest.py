import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def ingest_docs():
    pdf_loader = DirectoryLoader('./docs', glob="./*.pdf", loader_cls=PyPDFLoader)
    csv_loader = DirectoryLoader('./docs', glob="./*.csv", loader_cls=CSVLoader)
    loaders = {"pdf_loader": pdf_loader, "csv_loader": csv_loader}
    for loader in loaders:
        docs = loaders[loader].load()
        print(docs)
        if docs:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            
            content = [doc.page_content for doc in splits]
            metadata = [doc.metadata for doc in splits]
            ids = [f"id_{i}" for i in range(len(splits))]

            client = chromadb.PersistentClient(path="./data/chroma_db")
            ef = embedding_functions.DefaultEmbeddingFunction()

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
        else:
            print(f"no such file is present: for {loader}")

if __name__ == "__main__":
    ingest_docs()