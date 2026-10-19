"""Route calculator, memory-retrieval, and general chat requests."""
import re

from agents.calculator.agent import CalculatorError, calculate
from agents.agent1.agent import handle_message as handle_chat_message
from agents.memory.agent import format_memories, search_memory

_MEMORY_PREFIXES = (
    "memory ",
    "remember ",
    "recall ",
    "what did i ask about ",
    "what did we discuss about ",
    "show my history",
)
_PREFIXES = (
    "calculate ",
    "compute ",
    "what is ",
    "what's ",
    "solve ",
)
_EXPRESSION = re.compile(r"^[0-9\s.+*/%()\-]+$")


def route_message(user: str, message: str) -> str:
    """Route explicit memory requests, arithmetic, and other text to agents."""
    if not isinstance(message, str) or not message.strip():
        raise ValueError("message must be a non-empty string")
    if not isinstance(user, str) or not user.strip():
        raise ValueError("user must be a non-empty string")

    candidate = message.strip().lower()
    for prefix in _MEMORY_PREFIXES:
        if candidate.startswith(prefix):
            query = message.strip()[len(prefix):].strip()
            if prefix == "show my history":
                query = None
            records = search_memory(user, query=query)
            return format_memories(records)

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
