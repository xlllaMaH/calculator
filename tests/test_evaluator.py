import unittest

from calculator.evaluator import tokenize, evaluate


class TestTokenize(unittest.TestCase):

    def test_expression(self):
        self.assertEqual(tokenize("109 + 345 × 2"), ["109", "+", "345", "×", "2"])

    def test_without_spaces(self):
        self.assertEqual(tokenize("2+2×2"), ["2", "+", "2", "×", "2"])

    def test_numbers(self):
        self.assertEqual(tokenize("3.14"), ["3.14"])
        self.assertEqual(tokenize(".5"), [".5"])
        self.assertEqual(tokenize("3."), ["3."])

    def test_functions_and_brackets(self):
        self.assertEqual(tokenize("sqrt(4)"), ["sqrt", "(", "4", ")"])
        self.assertEqual(tokenize("-(1)^2"), ["-", "(", "1", ")", "^", "2"])

    def test_empty(self):
        self.assertEqual(tokenize(""), [])
        self.assertEqual(tokenize("   "), [])

    def test_invalid_symbol(self):
        # ASCII-операторы * и / вычислитель не понимает: их переводит KEY_MAP в окне
        for expression, symbol in [("2 * 3", "*"), ("2 / 3", "/"), ("SIN(30)", "S"), (".", ".")]:
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError) as ctx:
                    tokenize(expression)
                self.assertEqual(str(ctx.exception), f"Недопустимый символ: {symbol}")


class TestEvaluate(unittest.TestCase):

    def assertEvaluates(self, cases):
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.assertEqual(evaluate(expression), expected)

    def assertEvaluateRaises(self, expression, error, message):
        with self.assertRaises(error) as ctx:
            evaluate(expression)
        self.assertEqual(str(ctx.exception), message)

    def test_single_number(self):
        self.assertEvaluates([("42", 42), ("3.5", 3.5), (".5", 0.5)])

    def test_binary_operators(self):
        self.assertEvaluates([
            ("2 + 3", 5),
            ("2 - 3", -1),
            ("4 × 5", 20),
            ("7 ÷ 2", 3.5),
            ("7 % 3", 1),
            ("2 ^ 10", 1024),
        ])

    def test_precedence(self):
        self.assertEvaluates([
            ("109 + 345 × 2", 799),
            ("2 + 2 × 2", 6),
            ("10 - 6 ÷ 2", 7),
            ("2 × 3 ^ 2", 18),
            ("1 + 10 % 4", 3),
        ])

    def test_left_associativity(self):
        self.assertEvaluates([
            ("10 - 2 - 3", 5),
            ("100 ÷ 10 ÷ 2", 5),
            ("10 % 4 × 3", 6),
        ])

    def test_power_is_right_associative(self):
        self.assertEqual(evaluate("2 ^ 3 ^ 2"), 512)

    def test_brackets(self):
        self.assertEvaluates([
            ("(2 + 3) × 4", 20),
            ("2 × (3 + 4) ^ 2", 98),
            ("((1 + 2) × (3 + 4))", 21),
        ])

    def test_unary_minus(self):
        self.assertEvaluates([
            ("-5", -5),
            ("--3", 3),
            ("2 × -3", -6),
            ("-(2 + 3)", -5),
            # унарный минус слабее степени: -2^2 = -(2^2)
            ("-2 ^ 2", -4),
            ("(-2) ^ 2", 4),
            ("2 ^ -1", 0.5),
        ])

    def test_functions(self):
        self.assertEvaluates([
            ("sqrt(16)", 4),
            ("sqrt(16) + 1", 5),
            ("sqrt(sqrt(16))", 2),
            ("sin(30)", 0.5),
            ("cos(60)", 0.5),
            ("cos(90)", 0),
            ("floor(2.7)", 2),
            ("ceil(2.1)", 3),
            ("floor(-2.1)", -3),
            ("sqrt(3 × 3) × 2", 6),
        ])

    def test_whole_result_is_int(self):
        self.assertIsInstance(evaluate("4 ÷ 2"), int)
        self.assertIsInstance(evaluate("cos(90)"), int)
        self.assertIsInstance(evaluate("7 ÷ 2"), float)

    def test_result_is_rounded(self):
        self.assertEqual(evaluate("0.1 + 0.2"), 0.3)
        self.assertEqual(evaluate("1 ÷ 3"), 0.3333333333)

    def test_empty_expression(self):
        self.assertEvaluateRaises("", ValueError, "Пустое выражение")
        self.assertEvaluateRaises("   ", ValueError, "Пустое выражение")

    def test_incomplete_expression(self):
        self.assertEvaluateRaises("2 +", ValueError, "Неполное выражение")
        self.assertEvaluateRaises("-", ValueError, "Неполное выражение")

    def test_missing_bracket(self):
        self.assertEvaluateRaises("(2 + 3", ValueError, "Ожидалось: )")
        self.assertEvaluateRaises("sqrt(4", ValueError, "Ожидалось: )")
        self.assertEvaluateRaises("sin 30", ValueError, "Ожидалось: (")

    def test_extra_tokens(self):
        self.assertEvaluateRaises("2 3", ValueError, "Лишние символы в выражении")
        self.assertEvaluateRaises("(2) )", ValueError, "Лишние символы в выражении")
        self.assertEvaluateRaises("1.2.3", ValueError, "Лишние символы в выражении")

    def test_unexpected_token(self):
        self.assertEvaluateRaises("tan(45)", ValueError, "Неожиданный символ: tan")
        self.assertEvaluateRaises("× 2", ValueError, "Неожиданный символ: ×")

    def test_math_errors(self):
        self.assertEvaluateRaises("1 ÷ 0", ZeroDivisionError, "Деление на ноль")
        self.assertEvaluateRaises("5 % (2 - 2)", ZeroDivisionError, "Деление на ноль")
        self.assertEvaluateRaises("sqrt(-4)", ValueError, "Нельзя извлечь корень из отрицательного числа")


if __name__ == "__main__":
    unittest.main()
