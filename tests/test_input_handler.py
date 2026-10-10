import unittest

from calculator.operations.memory import m_clear, m_recall
from calculator.ui.buttons import BUTTONS
from calculator.ui.input_handler import InputHandler


class FakeDisplay:
    """Заменяет настоящий дисплей, чтобы тестировать обработчик без окна Tk."""

    def __init__(self):
        self.text = "0"

    def get(self):
        return self.text

    def set(self, value):
        self.text = value


class TestInputHandler(unittest.TestCase):

    def setUp(self):
        m_clear()
        self.display = FakeDisplay()
        self.handler = InputHandler(self.display)

    def tearDown(self):
        m_clear()

    def press(self, *keys):
        for key in keys:
            self.handler.press(key)
        return self.display.get()

    def test_typing_shows_expression(self):
        self.assertEqual(self.press("1", "2", "+", "3"), "12+3")
        self.assertEqual(self.handler.expression, "12+3")

    def test_equals(self):
        self.assertEqual(self.press("2", "+", "3", "×", "4", "="), "14")
        self.assertEqual(self.handler.expression, "14")

    def test_function_key(self):
        self.assertEqual(self.press("sqrt(", "9", ")", "="), "3")

    def test_digit_after_equals_starts_new_expression(self):
        self.assertEqual(self.press("2", "+", "3", "=", "7"), "7")

    def test_dot_after_equals_starts_new_expression(self):
        self.assertEqual(self.press("2", "+", "3", "=", ".", "5"), ".5")

    def test_function_after_equals_starts_new_expression(self):
        self.assertEqual(self.press("2", "+", "3", "=", "sin("), "sin(")

    def test_operator_after_equals_continues(self):
        self.assertEqual(self.press("2", "+", "3", "=", "×", "2", "="), "10")

    def test_clear(self):
        self.assertEqual(self.press("1", "2", "C"), "0")
        self.assertEqual(self.handler.expression, "")

    def test_backspace(self):
        self.assertEqual(self.press("1", "2", "3", "back"), "12")

    def test_backspace_to_empty_shows_zero(self):
        self.assertEqual(self.press("1", "back"), "0")
        self.assertEqual(self.press("back"), "0")

    def test_error_is_shown_and_expression_reset(self):
        self.assertEqual(self.press("1", "÷", "0", "="), "Деление на ноль")
        self.assertEqual(self.handler.expression, "")
        self.assertEqual(self.press("5"), "5")

    def test_invalid_expression(self):
        self.assertEqual(self.press("2", "+", "="), "Неполное выражение")
        self.assertEqual(self.press("="), "Пустое выражение")

    def test_overflow_does_not_crash(self):
        self.press("1", "0", "^", "4", "0", "0", "=")
        self.assertEqual(self.handler.expression, "")

    def test_memory_plus_and_recall(self):
        self.press("5", "m+")
        self.assertEqual(m_recall(), 5)
        # M+ не меняет дисплей
        self.assertEqual(self.display.get(), "5")
        self.assertEqual(self.press("C", "mr"), "5")

    def test_memory_evaluates_expression(self):
        self.press("2", "×", "3", "m+")
        self.assertEqual(m_recall(), 6)

    def test_memory_minus(self):
        self.press("1", "0", "m+", "C", "3", "m-")
        self.assertEqual(m_recall(), 7)

    def test_memory_clear(self):
        self.press("5", "m+", "mc")
        self.assertEqual(m_recall(), 0)

    def test_memory_with_empty_expression(self):
        self.press("m+")
        self.assertEqual(m_recall(), 0)

    def test_memory_with_invalid_expression(self):
        self.assertEqual(self.press("2", "+", "m+"), "Неполное выражение")
        self.assertEqual(m_recall(), 0)

    def test_recall_inside_expression(self):
        self.press("4", "m+", "C")
        self.assertEqual(self.press("1", "+", "mr", "="), "5")

    def test_every_button_key_is_handled(self):
        for _, key, *_ in BUTTONS:
            with self.subTest(key=key):
                InputHandler(FakeDisplay()).press(key)


if __name__ == "__main__":
    unittest.main()
