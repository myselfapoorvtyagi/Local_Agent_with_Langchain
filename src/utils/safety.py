import re
from pydantic import BaseModel, Field, validator

class SafetyReport(BaseModel):
    is_safe: bool = True
    reason: str = "Clear"

def pii_redaction_filter(text: str) -> str:
    """Basic regex-based PII redaction (Emails and Phone numbers)."""
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    redacted = re.sub(email_regex, "[EMAIL_REDACTED]", text)
    return redacted

def validate_response(answer: str):
    """Checks if the LLM output contains forbidden keywords."""
    forbidden = ["password", "secret_key", "internal_api"]
    for word in forbidden:
        if word in answer.lower():
            return False, f"Response contains sensitive keyword: {word}"
    return True, "Clear"