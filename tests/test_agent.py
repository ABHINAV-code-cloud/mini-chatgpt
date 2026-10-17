"""Unit tests for agent orchestration without external API calls."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

AGENT_PATH = Path(__file__).resolve().parents[1] / "agents" / "agent1" / "agent.py"

class AgentTests(unittest.TestCase):
    def setUp(self):
        self.ask_llm = Mock(return_value="Hello from the test model")
        self.save_memory = Mock()
        fake_llm = types.ModuleType("llm")
        fake_llm.ask_llm = self.ask_llm
        fake_memory = types.ModuleType("memstore.memory")
        fake_memory.save_memory = self.save_memory
        self.modules_patch = patch.dict(sys.modules, {"llm": fake_llm, "memstore.memory": fake_memory})
        self.modules_patch.start()
        spec = importlib.util.spec_from_file_location("agent_under_test", AGENT_PATH)
        self.agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.agent_module)

    def tearDown(self):
        self.modules_patch.stop()
        sys.modules.pop("agent_under_test", None)

    def test_handle_message_returns_model_reply(self):
        result = self.agent_module.handle_message("user-1", "Hi")
        self.assertEqual(result, "Hello from the test model")
        self.ask_llm.assert_called_once_with("Hi")

    def test_handle_message_saves_question_and_answer(self):
        self.agent_module.handle_message("user-1", "Hi")
        self.save_memory.assert_called_once_with("user-1", "Hi", "Hello from the test model")

if __name__ == "__main__":
    unittest.main()
