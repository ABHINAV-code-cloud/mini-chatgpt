"""Tests for user-scoped conversation memory retrieval."""
import json
import tempfile
import unittest
from pathlib import Path

from agents.memory.agent import format_memories, search_memory


class MemoryAgentTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_path = Path(self.temp_dir.name) / "memory.json"
        self.memory_path.write_text(json.dumps([
            {"user": "alice", "question": "How does JMeter measure throughput?", "answer": "Throughput is requests per unit time."},
            {"user": "bob", "question": "What is Python?", "answer": "A programming language."},
            {"user": "alice", "question": "Explain Python unit tests", "answer": "Tests verify expected behavior."},
        ]), encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_only_returns_records_for_requested_user(self):
        records = search_memory("alice", memory_file=self.memory_path)
        self.assertEqual(len(records), 2)
        self.assertTrue(all(item["user"] == "alice" for item in records))

    def test_query_ranks_relevant_records(self):
        records = search_memory("alice", query="JMeter throughput", memory_file=self.memory_path)
        self.assertEqual(records[0]["question"], "How does JMeter measure throughput?")

    def test_missing_file_returns_empty_history(self):
        missing = self.memory_path.parent / "missing.json"
        self.assertEqual(search_memory("alice", memory_file=missing), [])

    def test_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            search_memory("alice", limit=0, memory_file=self.memory_path)

    def test_formats_empty_results(self):
        self.assertIn("could not find", format_memories([]).lower())


if __name__ == "__main__":
    unittest.main()
