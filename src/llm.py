from langchain_ollama import ChatOllama

def get_model():
    return ChatOllama(
        model="qwen2.5:3b",
        temperature=0,
        base_url="http://localhost:11434"
    )