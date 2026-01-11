from langchain.tools import tool
from ..state import CalculatorInput

@tool(args_schema=CalculatorInput)
def calculator_tool(operation: str, a: float, b: float) -> str:
    """Performs basic arithmetic. Use this for ANY math-related queries."""
    if operation == "add":
        return str(a + b)
    elif operation == "subtract":
        return str(a - b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero."
        return str(a / b)
    else:
        return f"Unknown operation: {operation}"