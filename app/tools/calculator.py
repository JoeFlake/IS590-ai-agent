import ast
import math
import operator
from langchain.tools import tool
from app.logger import get_logger, log_tool_call, log_tool_error

_log = get_logger("tool.calculator")

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_FUNCTIONS = {
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "log": math.log, "log10": math.log10, "abs": abs,
    "ceil": math.ceil, "floor": math.floor, "exp": math.exp,
    "factorial": math.factorial, "pi": math.pi, "e": math.e,
}


def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        op = _OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        op = _OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(_eval(node.operand))
    if isinstance(node, ast.Call):
        name = node.func.id if isinstance(node.func, ast.Name) else None
        if name not in _FUNCTIONS:
            raise ValueError(f"Unknown function: {name}")
        return _FUNCTIONS[name](*[_eval(a) for a in node.args])
    if isinstance(node, ast.Name):
        if node.id in _FUNCTIONS:
            return _FUNCTIONS[node.id]
        raise ValueError(f"Unknown name: {node.id}")
    raise ValueError(f"Unsupported expression: {type(node).__name__}")


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Supports +, -, *, /, **, %, //
    and functions: sqrt, sin, cos, tan, log, log10, abs, ceil, floor, exp, factorial.
    Constants: pi, e. Example: 'sqrt(16) + 2 * pi'"""
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _eval(tree.body)
        result_str = str(result)
        log_tool_call(_log, "calculator", {"expression": expression}, result_str)
        return result_str
    except Exception as exc:
        log_tool_error(_log, "calculator", {"expression": expression}, str(exc))
        return f"Error: {exc}"
