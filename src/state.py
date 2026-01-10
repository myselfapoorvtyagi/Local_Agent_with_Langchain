from typing import Annotated, List, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

class CalculatorInput(BaseModel):
    """Input for the calculator tool."""
    operation: str = Field(description="The math operation to perform (e.g., 'add', 'multiply', 'divide')")
    a: float = Field(description="The first number")
    b: float = Field(description="The second number")

class AgentState(TypedDict):
    # 'add_messages' keeps history; Annotated ensures the graph knows how to update it
    messages: Annotated[list, add_messages]
    # Custom fields for our business logic
    is_safe: bool
    final_reasoning: str

class FinalResponse(BaseModel):
    """The structured output format for the user."""
    answer: str = Field(description="The validated answer")
    sources: List[str] = Field(default_factory=list)
    risk_score: int = Field(ge=0, le=10, description="Safety risk assessment")