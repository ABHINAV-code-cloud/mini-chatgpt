"""Safely evaluate basic arithmetic expressions without using eval."""
import ast
import operator
import re

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
_ALLOWED_CHARS = re.compile(r"^[0-9\s.+*/%()\-]+$")


class CalculatorError(ValueError):
    """Raised when an expression is not safe or cannot be evaluated."""


def calculate(expression: str):
    """Evaluate a numeric arithmetic expression using a restricted AST."""
    if not isinstance(expression, str) or not expression.strip():
        raise CalculatorError("Please provide an arithmetic expression.")
    expression = expression.strip()
    if len(expression) > 200 or not _ALLOWED_CHARS.fullmatch(expression):
        raise CalculatorError("Only basic arithmetic expressions are supported.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
    except (SyntaxError, ZeroDivisionError, OverflowError) as exc:
        raise CalculatorError("That arithmetic expression cannot be evaluated.") from exc
    except (TypeError, ValueError) as exc:
        if isinstance(exc, CalculatorError):
            raise
        raise CalculatorError("That arithmetic expression is invalid.") from exc

    if isinstance(result, complex) or not isinstance(result, (int, float)):
        raise CalculatorError("The result must be a real number.")
    if abs(result) > 1e100:
        raise CalculatorError("The result is too large.")
    return result


def _evaluate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise CalculatorError("Exponent is too large.")
        return _OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    raise CalculatorError("Only basic arithmetic expressions are supported.")
