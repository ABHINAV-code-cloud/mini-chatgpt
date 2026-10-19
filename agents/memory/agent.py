"""Retrieve relevant saved conversation records for one user."""
import json
import re
from pathlib import Path
from typing import Any

from memstore.memory import MEMORY_FILE

_WORDS = re.compile(r"[a-zA-Z0-9_]+")


def search_memory(
    user: str,
    query: str | None = None,
    limit: int = 5,
    memory_file: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Return recent or query-matching records belonging only to user.

    A missing memory file is treated as an empty history. Corrupt JSON is
    reported as ValueError rather than silently discarded.
    """
    if not isinstance(user, str) or not user.strip():
        raise ValueError("user must be a non-empty string")
    if query is not None and not isinstance(query, str):
        raise ValueError("query must be text or None")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 20:
        raise ValueError("limit must be an integer between 1 and 20")

    path = Path(memory_file) if memory_file is not None else Path(MEMORY_FILE)
    try:
        with path.open("r", encoding="utf-8") as handle:
            records = json.load(handle)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        raise ValueError("conversation memory file contains invalid JSON") from exc

    if not isinstance(records, list):
        raise ValueError("conversation memory must be a JSON list")

    user_records = [
        item for item in records
        if isinstance(item, dict) and item.get("user") == user
    ]

    if query and query.strip():
        terms = {word.lower() for word in _WORDS.findall(query) if len(word) > 1}
        if terms:
            ranked = []
            for item in user_records:
                searchable = f"{item.get('question', '')} {item.get('answer', '')}"
                words = {word.lower() for word in _WORDS.findall(searchable)}
                overlap = len(terms & words)
                if overlap:
                    ranked.append((overlap / len(terms), item))
            ranked.sort(key=lambda pair: pair[0], reverse=True)
            return [dict(item) for _, item in ranked[:limit]]

    return [dict(item) for item in reversed(user_records[-limit:])]


def format_memories(records: list[dict[str, Any]]) -> str:
    """Format retrieved records as a readable plain-text response."""
    if not records:
        return "I could not find any matching saved conversations."
    lines = []
    for index, item in enumerate(records, start=1):
        question = str(item.get("question", "")).strip()
        answer = str(item.get("answer", "")).strip()
        lines.append(f"{index}. You asked: {question}\n   Previous answer: {answer}")
    return "\n".join(lines)
