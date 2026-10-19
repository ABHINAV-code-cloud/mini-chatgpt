"""Search supplied documents for passages relevant to a query.

This agent is intentionally deterministic and offline: callers supply a mapping
of document names to text. It does not browse the web or execute document code.
"""
from collections.abc import Mapping
import re
from typing import Any

_WORDS = re.compile(r"[a-zA-Z0-9_]+")


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in _WORDS.findall(text) if len(token) > 1}


def search_documents(query: str, documents: Mapping[str, str], limit: int = 3) -> list[dict[str, Any]]:
    """Return the best matching document snippets ranked by query-token overlap.

    Args:
        query: Search query supplied by the user.
        documents: Mapping of document name to plain-text content.
        limit: Maximum number of results to return (1-10).

    Returns:
        A list of dictionaries containing document, score, and snippet.
        Empty list means no relevant documents were found.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    if not isinstance(documents, Mapping):
        raise TypeError("documents must be a mapping of names to text")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 10:
        raise ValueError("limit must be an integer between 1 and 10")

    query_tokens = _tokens(query)
    if not query_tokens:
        return []

    results = []
    for name, content in documents.items():
        if not isinstance(name, str) or not isinstance(content, str):
            continue
        content_tokens = _tokens(content)
        matched = query_tokens & content_tokens
        if not matched:
            continue

        # Simple, interpretable score: fraction of query terms present.
        score = len(matched) / len(query_tokens)
        snippet = _make_snippet(content, matched)
        results.append({
            "document": name,
            "score": round(score, 4),
            "matched_terms": sorted(matched),
            "snippet": snippet,
        })

    results.sort(key=lambda item: (-item["score"], item["document"].lower()))
    return results[:limit]


def _make_snippet(content: str, matched_terms: set[str], width: int = 240) -> str:
    """Choose a short passage around the first matching term."""
    lowered = content.lower()
    positions = [lowered.find(term) for term in matched_terms if lowered.find(term) >= 0]
    if not positions:
        return content[:width].strip()
    start = max(0, min(positions) - width // 4)
    end = min(len(content), start + width)
    snippet = content[start:end].strip()
    if start:
        snippet = "…" + snippet
    if end < len(content):
        snippet += "…"
    return snippet
