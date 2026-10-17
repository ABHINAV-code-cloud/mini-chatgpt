"""Unit tests for JSON memory persistence using temporary files."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from memstore import memory

class MemoryTests(unittest.TestCase):
    def test_save_memory_creates_file_and_stores_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            memory_path = Path(temp_dir) / "memory.json"
            with patch.object(memory, "MEMORY_FILE", str(memory_path)):
                memory.save_memory("user-1", "question", "answer")
            records = json.loads(memory_path.read_text(encoding="utf-8"))
            self.assertEqual(records, [{"user": "user-1", "question": "question", "answer": "answer"}])

    def test_save_memory_appends_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            memory_path = Path(temp_dir) / "memory.json"
            with patch.object(memory, "MEMORY_FILE", str(memory_path)):
                memory.save_memory("user-1", "first", "one")
                memory.save_memory("user-2", "second", "two")
            records = json.loads(memory_path.read_text(encoding="utf-8"))
            self.assertEqual(len(records), 2)
            self.assertEqual(records[1]["question"], "second")

if __name__ == "__main__":
    unittest.main()
