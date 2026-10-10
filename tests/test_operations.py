import unittest

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
from calculator.operations.memory import m_plus, m_minus, m_recall, m_clear


class TestArithmetic(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-2, 3), 1)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)
        self.assertEqual(subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(multiply(4, 5), 20)
        self.assertEqual(multiply(-4, 5), -20)
        self.assertEqual(multiply(7, 0), 0)
        self.assertAlmostEqual(multiply(0.5, 0.5), 0.25)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(7, 2), 3.5)
        self.assertEqual(divide(-9, 3), -3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError) as ctx:
            divide(1, 0)
        self.assertEqual(str(ctx.exception), "Деление на ноль")

    def test_modulo(self):
        self.assertEqual(modulo(7, 3), 1)
        self.assertEqual(modulo(10, 5), 0)
        self.assertEqual(modulo(7.5, 2), 1.5)

    def test_modulo_by_zero(self):
        with self.assertRaises(ZeroDivisionError) as ctx:
            modulo(5, 0)
        self.assertEqual(str(ctx.exception), "Деление на ноль")

    def test_power(self):
        self.assertEqual(power(2, 10), 1024)
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(2, -1), 0.5)
        self.assertEqual(power(9, 0.5), 3)


class TestFunctions(unittest.TestCase):

    def test_sin_uses_degrees(self):
        self.assertAlmostEqual(sin(0), 0)
        self.assertAlmostEqual(sin(30), 0.5)
        self.assertAlmostEqual(sin(90), 1)
        self.assertAlmostEqual(sin(-90), -1)

    def test_cos_uses_degrees(self):
        self.assertAlmostEqual(cos(0), 1)
        self.assertAlmostEqual(cos(60), 0.5)
        self.assertAlmostEqual(cos(90), 0)
        self.assertAlmostEqual(cos(180), -1)

    def test_sqrt(self):
        self.assertEqual(sqrt(16), 4)
        self.assertEqual(sqrt(0), 0)
        self.assertAlmostEqual(sqrt(2), 1.41421356, places=8)

    def test_sqrt_of_negative(self):
        with self.assertRaises(ValueError) as ctx:
            sqrt(-1)
        self.assertEqual(str(ctx.exception), "Нельзя извлечь корень из отрицательного числа")

    def test_floor(self):
        self.assertEqual(floor(2.7), 2)
        self.assertEqual(floor(-2.1), -3)
        self.assertEqual(floor(5), 5)

    def test_ceil(self):
        self.assertEqual(ceil(2.1), 3)
        self.assertEqual(ceil(-2.7), -2)
        self.assertEqual(ceil(5), 5)


class TestMemory(unittest.TestCase):

    # глобальное состояние модуля, поэтому очищаем её вокруг каждого теста
    def setUp(self):
        m_clear()

    def tearDown(self):
        m_clear()

    def test_starts_empty(self):
        self.assertEqual(m_recall(), 0)

    def test_m_plus(self):
        self.assertEqual(m_plus(5), 5)
        self.assertEqual(m_plus(2.5), 7.5)
        self.assertEqual(m_recall(), 7.5)

    def test_m_minus(self):
        m_plus(10)
        self.assertEqual(m_minus(3), 7)
        self.assertEqual(m_minus(10), -3)
        self.assertEqual(m_recall(), -3)

    def test_m_clear(self):
        m_plus(42)
        m_clear()
        self.assertEqual(m_recall(), 0)


if __name__ == "__main__":
    unittest.main()
