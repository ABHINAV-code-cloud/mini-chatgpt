"""Agent entry point for generating replies and storing conversation history."""
import logging

from llm import ask_llm
from memstore.memory import save_memory

logger = logging.getLogger(__name__)

LLM_ERROR_REPLY = (
    "Sorry, I couldn't generate a response right now. Please try again."
)


def handle_message(user, message):
    """Generate a reply, then best-effort persist the conversation.

    Invalid input raises ValueError. LLM failures return a safe user-facing
    message and do not save a failed exchange. Memory failures are logged but
    do not discard a reply that was already generated successfully.
    """
    if not isinstance(user, str) or not user.strip():
        raise ValueError("user must be a non-empty string")
    if not isinstance(message, str) or not message.strip():
        raise ValueError("message must be a non-empty string")

    try:
        reply = ask_llm(message)
    except Exception:
        logger.exception("LLM request failed")
        return LLM_ERROR_REPLY

    try:
        save_memory(user, message, reply)
    except Exception:
        logger.exception("Could not save conversation memory")

    return reply
