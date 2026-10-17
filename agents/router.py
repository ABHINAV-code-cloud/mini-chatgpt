"""Route straightforward arithmetic requests to the calculator agent."""
import re

from agents.calculator.agent import CalculatorError, calculate
from agents.agent1.agent import handle_message as handle_chat_message

_PREFIXES = (
    "calculate ",
    "compute ",
    "what is ",
    "what's ",
    "solve ",
)
_EXPRESSION = re.compile(r"^[0-9\s.+*/%()\-]+$")


def route_message(user: str, message: str) -> str:
    """Route arithmetic-only requests to calculator; all other text to chat."""
    if not isinstance(message, str) or not message.strip():
        raise ValueError("message must be a non-empty string")

    candidate = message.strip().lower()
    for prefix in _PREFIXES:
        if candidate.startswith(prefix):
            candidate = candidate[len(prefix):].strip()
            break

    if _EXPRESSION.fullmatch(candidate) and any(ch.isdigit() for ch in candidate):
        try:
            return str(calculate(candidate))
        except CalculatorError as exc:
            return f"Could not calculate that expression: {exc}"

    return handle_chat_message(user, message)
