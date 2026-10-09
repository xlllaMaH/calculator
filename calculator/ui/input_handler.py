from calculator.evaluator import evaluate
from calculator.operations.memory import m_plus, m_minus, m_recall, m_clear


class InputHandler:
    """Принимает нажатия кнопок, собирает выражение и показывает его на дисплее."""

    def __init__(self, display):
        self.display = display
        self.expression = ""
        self.just_evaluated = False

    def press(self, key):
        try:
            self._handle(key)
        except (ValueError, ArithmeticError) as error:
            self.expression = ""
            self.just_evaluated = False
            self.display.set(str(error))

    def _handle(self, key):
        if key == "=":
            result = evaluate(self.expression)
            self.expression = str(result)
            self.just_evaluated = True
            self.display.set(self.expression)
        elif key == "C":
            self.expression = ""
            self.just_evaluated = False
            self.display.set("0")
        elif key == "back":
            self.expression = self.expression[:-1]
            self.display.set(self.expression or "0")
        elif key == "mc":
            m_clear()
        elif key == "mr":
            self._append(str(m_recall()))
        elif key == "m+":
            m_plus(evaluate(self.expression or "0"))
        elif key == "m-":
            m_minus(evaluate(self.expression or "0"))
        else:
            self._append(key)

    def _append(self, text):
        # после "=" цифра или функция начинают новое выражение, а оператор продолжает старое
        if self.just_evaluated and (text[0].isdigit() or text[0] == "." or text.endswith("(")):
            self.expression = ""
        self.just_evaluated = False
        self.expression += text
        self.display.set(self.expression)
