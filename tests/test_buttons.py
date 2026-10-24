import pytest

from calculator.ui.display import WIDTH


def buttons(text):
    """'1 2 + 3' -> ['1', '2', '+', '3']: последовательность нажатий одной строкой."""
    return text.split()


# --- набор выражения ---

def test_digits_appear_on_display(app):
    assert app.click("1", "2", "3") == "123"


def test_first_digit_replaces_zero(app):
    assert app.click("7") == "7"


def test_expression_is_shown_as_typed(app):
    assert app.click(*buttons("1 2 + 3 × 4")) == "12+3×4"


@pytest.mark.parametrize("label, text", [
    ("√", "sqrt("), ("sin", "sin("), ("cos", "cos("), ("⌊x⌋", "floor("), ("⌈x⌉", "ceil("),
])
def test_function_button_opens_bracket(app, label, text):
    assert app.click(label) == text


def test_long_input_is_cut_from_the_left(app):
    # набрано 1111111111+2222222222 (21 символ), влезают только последние
    app.click(*["1"] * 10, "+", *["2"] * 10)
    assert app.screen() == "…111+2222222222"
    assert len(app.screen()) == WIDTH


def test_input_of_max_width_is_not_cut(app):
    assert app.click(*["9"] * WIDTH) == "9" * WIDTH


# --- вычисления ---

@pytest.mark.parametrize("pressed, result", [
    # простые операции
    ("2 + 3", "5"),
    ("2 - 3", "-1"),
    ("4 × 5", "20"),
    ("7 ÷ 2", "3.5"),
    ("7 % 3", "1"),
    ("2 ^ 1 0", "1024"),
    ("1 . 5 + 1", "2.5"),
    # приоритет операций
    ("2 + 2 × 2", "6"),
    ("1 0 - 6 ÷ 2", "7"),
    ("2 × 3 ^ 2", "18"),
    ("2 ^ 3 ^ 2", "512"),
    ("1 0 - 2 - 3", "5"),
    # скобки
    ("( 2 + 2 ) × 2", "8"),
    ("2 × ( 3 + 4 ) ^ 2", "98"),
    # отрицательные числа
    ("- 5 × 2", "-10"),
    ("2 × - 3", "-6"),
    ("- 2 ^ 2", "-4"),
    ("( - 2 ) ^ 2", "4"),
    # функции, углы в градусах
    ("√ 1 6 )", "4"),
    ("√ 1 6 ) + 1", "5"),
    ("sin 3 0 )", "0.5"),
    ("cos 6 0 )", "0.5"),
    ("cos 9 0 )", "0"),
    ("⌊x⌋ 2 . 7 )", "2"),
    ("⌈x⌉ 2 . 1 )", "3"),
    ("⌊x⌋ - 2 . 1 )", "-3"),
    # целый результат без дробной части, дробный — округлён
    ("8 ÷ 4", "2"),
    ("2 . 5 × 2", "5"),
    (". 1 + . 2", "0.3"),
    ("1 ÷ 3", "0.3333333333"),
])
def test_calculation(app, pressed, result):
    assert app.click(*buttons(pressed), "=") == result


def test_long_result_is_cut_from_the_left(app):
    app.click(*buttons("2 ^ 6 0 ="))
    assert app.screen() == "…" + str(2 ** 60)[-(WIDTH - 1):]


# --- что происходит после "=" ---

@pytest.fixture
def after_result(app):
    app.click(*buttons("2 + 3 ="))
    return app


def test_digit_after_result_starts_new_expression(after_result):
    assert after_result.click("7") == "7"


def test_dot_after_result_starts_new_expression(after_result):
    assert after_result.click(".", "5") == ".5"


def test_function_after_result_starts_new_expression(after_result):
    assert after_result.click("√") == "sqrt("


def test_operator_after_result_continues_with_it(after_result):
    assert after_result.click("×", "2") == "5×2"
    assert after_result.click("=") == "10"


def test_equals_again_keeps_result(after_result):
    assert after_result.click("=") == "5"


# --- C и ⌫ ---

def test_clear(app):
    assert app.click(*buttons("1 2 + C")) == "0"


def test_new_calculation_after_clear(app):
    assert app.click(*buttons("9 9 C 2 + 2 =")) == "4"


def test_backspace_removes_last_symbol(app):
    assert app.click(*buttons("1 2 3 ⌫")) == "12"


def test_backspace_to_empty_shows_zero(app):
    assert app.click("1", "⌫") == "0"
    assert app.click("⌫") == "0"


def test_fix_typo_with_backspace(app):
    assert app.click(*buttons("2 + ⌫ × 3 =")) == "6"


# --- ошибки ---

@pytest.mark.parametrize("pressed, message", [
    ("1 ÷ 0 =", "Деление на ноль"),
    ("5 % 0 =", "Деление на ноль"),
    ("√ - 4 ) =", "Нельзя извлечь корень из отрицательного числа"),
    ("2 + =", "Неполное выражение"),
    ("=", "Пустое выражение"),
    ("( 2 + 3 =", "Ожидалось: )"),
    ("2 ) =", "Лишние символы в выражении"),
    (". =", "Недопустимый символ: ."),
])
def test_error_message_is_shown(app, pressed, message):
    assert app.click(*buttons(pressed)) == message


def test_typing_after_error_starts_new_expression(app):
    app.click(*buttons("1 ÷ 0 ="))
    assert app.click("5") == "5"
    assert app.click("+", "1", "=") == "6"


def test_app_keeps_working_after_overflow(app):
    app.click(*buttons("1 0 ^ 4 0 0 ="))
    assert app.screen() != "10^400"
    assert app.click(*buttons("2 + 2 =")) == "4"


# --- память ---

def recall(app):
    return app.click("C", "MR")


def test_memory_is_empty_on_start(app):
    assert recall(app) == "0"


def test_m_plus_and_recall(app):
    app.click("5", "M+")
    assert recall(app) == "5"


def test_m_plus_does_not_change_display(app):
    assert app.click("5", "M+") == "5"


def test_m_plus_accumulates(app):
    app.click(*buttons("5 M+ C 3 M+"))
    assert recall(app) == "8"


def test_m_minus(app):
    app.click(*buttons("1 0 M+ C 3 M-"))
    assert recall(app) == "7"


def test_memory_saves_result_of_expression(app):
    app.click(*buttons("2 × 3 M+"))
    assert recall(app) == "6"


def test_memory_clear(app):
    app.click(*buttons("5 M+ MC"))
    assert recall(app) == "0"


def test_memory_survives_clear(app):
    app.click(*buttons("4 M+ C C"))
    assert recall(app) == "4"


def test_recall_inside_expression(app):
    app.click(*buttons("4 M+ C"))
    assert app.click(*buttons("1 + MR")) == "1+4"
    assert app.click("=") == "5"


def test_m_plus_with_wrong_expression_shows_error(app):
    assert app.click(*buttons("2 + M+")) == "Неполное выражение"
    assert recall(app) == "0"
