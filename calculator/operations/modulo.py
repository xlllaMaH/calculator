def modulo(a, b):
    if b == 0:
        raise ZeroDivisionError("Деление на ноль")
    return a & b