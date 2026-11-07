_memory = 0


def m_plus(x):
    """M+: прибавить x к значению в памяти."""
    global _memory
    _memory += x
    return _memory


def m_minus(x):
    """M-: вычесть x из значения в памяти."""
    global _memory
    _memory -= x
    return _memory


def m_recall():
    """MR: вернуть значение из памяти."""
    return _memory


def m_clear():
    """MC: очистить память."""
    global _memory
    _memory = 0
