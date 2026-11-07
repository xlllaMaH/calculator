# calculator/evaluator.py
import re

from calculator.operations.add import add
from calculator.operations.subtract import subtract
from calculator.operations.multiply import multiply
from calculator.operations.divide import divide
from calculator.operations.modulo import modulo
from calculator.operations.power import power
from calculator.operations.sin import sin
from calculator.operations.cos import cos
from calculator.operations.sqrt import sqrt
from calculator.operations.floor import floor
from calculator.operations.ceil import ceil

BINARY = {"+": add, "-": subtract, "×": multiply, "÷": divide, "%": modulo, "^": power}
FUNCTIONS = {"sin": sin, "cos": cos, "sqrt": sqrt, "floor": floor, "ceil": ceil}
TOKEN = re.compile(r"\s*(\d+\.?\d*|\.\d+|[a-z]+|[+\-×÷%^()])")


def tokenize(expression):
    """Разбивает строку на числа, операторы, скобки и имена функций."""
    expression = expression.strip()
    tokens = []
    pos = 0
    while pos < len(expression):
        match = TOKEN.match(expression, pos)
        if not match:
            raise ValueError(f"Недопустимый символ: {expression[pos:].lstrip()[0]}")
        tokens.append(match.group(1))
        pos = match.end()
    return tokens


def evaluate(expression):
    """Считает выражение с учётом приоритетов, скобок и функций.

    Пример: evaluate("109 + 345 × 2") -> 799
    Приоритет (от низшего): + -  |  × ÷ %  |  унарный минус  |  ^
    """
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Пустое выражение")
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def take():
        nonlocal pos
        token = peek()
        pos += 1
        return token

    def expect(token):
        if take() != token:
            raise ValueError(f"Ожидалось: {token}")

    def expr():  # + -
        value = term()
        while peek() in ("+", "-"):
            op = take()
            value = BINARY[op](value, term())
        return value

    def term():  # × ÷ %
        value = unary()
        while peek() in ("×", "÷", "%"):
            op = take()
            value = BINARY[op](value, unary())
        return value

    def unary():  # унарный минус
        if peek() == "-":
            take()
            return -unary()
        return pwr()

    def pwr():  # ^ (правоассоциативная)
        base = atom()
        if peek() == "^":
            take()
            return power(base, unary())
        return base

    def atom():  # число, (выражение) или функция(выражение)
        token = take()
        if token is None:
            raise ValueError("Неполное выражение")
        if token == "(":
            value = expr()
            expect(")")
            return value
        if token in FUNCTIONS:
            expect("(")
            value = expr()
            expect(")")
            return FUNCTIONS[token](value)
        try:
            return float(token)
        except ValueError:
            raise ValueError(f"Неожиданный символ: {token}")

    result = expr()
    if pos != len(tokens):
        raise ValueError("Лишние символы в выражении")
    result = round(result, 10)
    return int(result) if result == int(result) else result
