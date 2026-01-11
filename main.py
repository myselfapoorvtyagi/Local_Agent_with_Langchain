import sys
from src.agent import build_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage

def run_interactive_chat():
    workflow = build_agent()
    # Path to your persistent database
    db_path = "./data/checkpoints.db"
    
    with SqliteSaver.from_conn_string(db_path) as memory:
        app = workflow.compile(checkpointer=memory, interrupt_before=["action"])
        
        # Use a fixed thread_id for the ongoing conversation
        config = {"configurable": {"thread_id": "chat_session_001"}}
        
        print("--- 🤖 Local Agent Started (type 'exit' or 'quit' to stop) ---")
        
        while True:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # 1. Process User Input
            inputs = {"messages": [HumanMessage(content=user_input)]}
            
            for event in app.stream(inputs, config, stream_mode="values"):
                # Print the assistant's thinking/responses as they come
                last_msg = event["messages"][-1]
                if last_msg.type == "ai" and not last_msg.tool_calls:
                    print(f"\nAgent: {last_msg.content}")

            # 2. Check for HITL (Wait for approval if tool is called)
            snapshot = app.get_state(config)
            while snapshot.next:
                # This part handles the 'action' node interruption
                last_msg = snapshot.values["messages"][-1]
                print(f"\n[SYSTEM]: Agent wants to use tools: {last_msg.tool_calls[0]['name']}")
                choice = input("Proceed? (y/n/edit): ").lower()
                
                if choice == 'y':
                    # Resume execution
                    for event in app.stream(None, config, stream_mode="values"):
                        last_msg = event["messages"][-1]
                        if last_msg.type == "ai" and not last_msg.tool_calls:
                            print(f"\nAgent: {last_msg.content}")
                else:
                    print("Action cancelled. You can provide further instructions.")
                    break
                
                # Refresh snapshot to see if there are more tools to run
                snapshot = app.get_state(config)

if __name__ == "__main__":
    run_interactive_chat()