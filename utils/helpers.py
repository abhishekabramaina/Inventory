from typing import Any, Dict

def sanitize_input(user_input: str) -> str:
    """Sanitizes user input string by stripping surrounding whitespace."""
    return user_input.strip()

def format_response(data: Any) -> Dict[str, Any]:
    """Formats payload as a standardized success API response dict."""
    return {"status": "success", "data": data}

def format_error(message: str) -> Dict[str, Any]:
    """Formats an error message as a standardized error API response dict."""
    return {"status": "error", "message": message}