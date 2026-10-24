import pytest

from calculator.evaluator import tokenize, evaluate

# правила разбора выражения, которые реализует сам вычислитель


def test_tokenize_splits_expression():
    assert tokenize(" sqrt(2.5)+.5×3 ") == ["sqrt", "(", "2.5", ")", "+", ".5", "×", "3"]


@pytest.mark.parametrize("expression, symbol", [("2 * 3", "*"), ("2/3", "/"), ("SIN(30)", "S")])
def test_tokenize_points_to_wrong_symbol(expression, symbol):
    with pytest.raises(ValueError) as error:
        tokenize(expression)
    assert str(error.value) == f"Недопустимый символ: {symbol}"


@pytest.mark.parametrize("expression, result", [
    # от низшего приоритета к высшему: + -  |  × ÷ %  |  унарный минус  |  ^
    ("1 + 2 × 3 ^ 2", 19),
    ("10 - 4 % 3 × 2", 8),
    ("2 ^ 3 ^ 2", 512),
    ("-2 ^ 2", -4),
    ("2 ^ -1", 0.5),
    ("--3", 3),
    ("sqrt(sqrt(16)) × (1 + (2 + 3))", 12),
    ("sin(30) + cos(60)", 1),
])
def test_evaluate(expression, result):
    assert evaluate(expression) == result


def test_result_type():
    assert isinstance(evaluate("4 ÷ 2"), int)
    assert isinstance(evaluate("7 ÷ 2"), float)


@pytest.mark.parametrize("expression, message", [
    ("tan(45)", "Неожиданный символ: tan"),
    ("sin 30", "Ожидалось: ("),
    ("1.2.3", "Лишние символы в выражении"),
])
def test_evaluate_error(expression, message):
    with pytest.raises(ValueError) as error:
        evaluate(expression)
    assert str(error.value) == message
