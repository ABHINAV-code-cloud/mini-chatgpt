"""Tests for offline document search."""
import unittest

from agents.research.agent import search_documents


class ResearchAgentTests(unittest.TestCase):
    def setUp(self):
        self.documents = {
            "performance.md": "JMeter load testing measures throughput, latency, and error rate.",
            "python.md": "Python supports functions, classes, and automated unit tests.",
            "empty.md": "",
        }

    def test_ranks_document_with_most_query_terms(self):
        results = search_documents(
            "JMeter load testing throughput",
            self.documents,
        )
        self.assertTrue(results)
        self.assertEqual(results[0]["document"], "performance.md")
        self.assertEqual(results[0]["score"], 1.0)

    def test_returns_empty_when_nothing_matches(self):
        self.assertEqual(search_documents("volcano astronomy", self.documents), [])

    def test_rejects_empty_query(self):
        with self.assertRaisesRegex(ValueError, "non-empty string"):
            search_documents(" ", self.documents)

    def test_rejects_invalid_limit(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 10"):
            search_documents("python", self.documents, limit=0)

    def test_limits_results(self):
        results = search_documents(
            "testing",
            self.documents,
            limit=1,
        )
        self.assertLessEqual(len(results), 1)

    def test_ignores_non_text_document_values(self):
        results = search_documents("python", {"valid.md": "Python code", "bad": None})
        self.assertEqual(results[0]["document"], "valid.md")


if __name__ == "__main__":
    unittest.main()
