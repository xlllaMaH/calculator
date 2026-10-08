import math


def sqrt(x):
    if x < 0:
        raise ValueError("Нельзя извлечь корень из отрицательного числа")
    return math.sqrt(x)
