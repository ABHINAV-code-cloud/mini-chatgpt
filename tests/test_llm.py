"""Unit tests for the OpenAI adapter; no network calls or real API key needed."""
import os
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import llm


class LlmTests(unittest.TestCase):
    def test_missing_api_key_fails_with_clear_message(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "OPENAI_API_KEY is not set"):
                llm.ask_llm("hello")

    def test_uses_client_and_returns_reply(self):
        create = Mock(return_value=SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="Test reply"))]
        ))
        client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(create=create)
            )
        )
        openai_module = types.ModuleType("openai")
        openai_module.OpenAI = Mock(return_value=client)

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "OPENAI_MODEL": "test-model"}):
            with patch.dict(sys.modules, {"openai": openai_module}):
                result = llm.ask_llm("hello")

        self.assertEqual(result, "Test reply")
        openai_module.OpenAI.assert_called_once_with(api_key="test-key")
        create.assert_called_once_with(
            model="test-model",
            messages=[{"role": "user", "content": "hello"}],
        )


if __name__ == "__main__":
    unittest.main()
