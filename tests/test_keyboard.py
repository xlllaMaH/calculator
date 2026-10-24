import pytest

# окну посылаются настоящие нажатия клавиш, как будто пользователь печатает


def test_digits(shown_app):
    assert shown_app.press_keys(*"1234567890") == "1234567890"


@pytest.mark.parametrize("keysym, text", [
    ("plus", "+"),
    ("minus", "-"),
    ("percent", "%"),
    ("asciicircum", "^"),
    ("period", "."),
    ("parenleft", "("),
    ("parenright", ")"),
    # * и / с клавиатуры превращаются в знаки калькулятора
    ("asterisk", "×"),
    ("slash", "÷"),
])
def test_symbol_keys(shown_app, keysym, text):
    assert shown_app.press_keys(keysym) == text


@pytest.mark.parametrize("enter", ["Return", "KP_Enter"])
def test_enter_calculates(shown_app, enter):
    assert shown_app.press_keys("1", "2", "asterisk", "3", enter) == "36"


def test_backspace(shown_app):
    assert shown_app.press_keys("1", "2", "3", "BackSpace") == "12"


def test_escape_clears(shown_app):
    assert shown_app.press_keys("1", "2", "Escape") == "0"


@pytest.mark.parametrize("keysym", ["s", "q", "x", "at", "space", "comma", "equal"])
def test_other_keys_are_ignored(shown_app, keysym):
    assert shown_app.press_keys("1", keysym) == "1"


def test_error_from_keyboard(shown_app):
    assert shown_app.press_keys("1", "slash", "0", "Return") == "Деление на ноль"


def test_keyboard_and_buttons_together(shown_app):
    shown_app.press_keys("2")
    shown_app.click("+")
    shown_app.press_keys("3")
    shown_app.click("×")
    assert shown_app.press_keys("4", "Return") == "14"
