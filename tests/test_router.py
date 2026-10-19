"""Tests for routing between calculator, memory, and chat agents."""
import unittest
from unittest.mock import patch

from agents.calculator.agent import CalculatorError, calculate
from agents.router import route_message


class CalculatorTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(calculate("2 + 3 * 4"), 14)

    def test_parentheses(self):
        self.assertEqual(calculate("(2 + 3) * 4"), 20)

    def test_division_by_zero_is_rejected(self):
        with self.assertRaises(CalculatorError):
            calculate("10 / 0")

    def test_code_execution_is_rejected(self):
        with self.assertRaises(CalculatorError):
            calculate("__import__('os').system('echo unsafe')")


class RouterTests(unittest.TestCase):
    @patch("agents.router.handle_chat_message", return_value="chat reply")
    def test_arithmetic_routes_to_calculator(self, chat):
        self.assertEqual(route_message("user-1", "calculate 2 + 2"), "4")
        chat.assert_not_called()

    @patch("agents.router.handle_chat_message", return_value="chat reply")
    def test_general_question_routes_to_chat(self, chat):
        self.assertEqual(route_message("user-1", "Explain Python"), "chat reply")
        chat.assert_called_once_with("user-1", "Explain Python")

    @patch("agents.router.format_memories", return_value="found memories")
    @patch("agents.router.search_memory", return_value=[{"question": "JMeter?"}])
    @patch("agents.router.handle_chat_message")
    def test_memory_prefix_routes_to_memory_agent(self, chat, search, format_results):
        self.assertEqual(route_message("user-1", "memory JMeter"), "found memories")
        search.assert_called_once_with("user-1", query="JMeter")
        format_results.assert_called_once()
        chat.assert_not_called()

    @patch("agents.router.format_memories", return_value="history")
    @patch("agents.router.search_memory", return_value=[])
    def test_show_history_requests_recent_records(self, search, format_results):
        self.assertEqual(route_message("user-1", "show my history"), "history")
        search.assert_called_once_with("user-1", query=None)

    def test_empty_message_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "message must be a non-empty string"):
            route_message("user-1", "  ")

    def test_empty_user_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "user must be a non-empty string"):
            route_message(" ", "hello")


if __name__ == "__main__":
    unittest.main()
