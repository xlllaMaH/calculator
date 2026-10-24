import pytest

# как кнопки должны выглядеть на экране: строка за строкой, слева направо
LAYOUT = [
    ["MC", "MR", "M+", "M-"],
    ["sin", "cos", "√", "^"],
    ["⌊x⌋", "⌈x⌉", "(", ")"],
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", "0", ".", "="],
]
CELLS = [
    (label, row, column)
    for row, labels in enumerate(LAYOUT)
    for column, label in enumerate(labels)
]
LABELS = list(dict.fromkeys(label for label, _, _ in CELLS))


def test_title(app):
    assert app.window.title() == "Калькулятор"


def test_window_is_not_resizable(app):
    assert app.window.resizable() == (0, 0)


def test_display_shows_zero_on_start(app):
    assert app.screen() == "0"


def test_display_is_right_aligned(app):
    assert app.window.display.cget("anchor") == "e"


def test_display_spans_whole_width_at_the_top(app):
    info = app.window.display.grid_info()
    assert (info["row"], info["column"], info["columnspan"]) == (0, 0, 4)


def test_has_exactly_the_expected_buttons(app):
    assert sorted(app.buttons) == sorted(LABELS)


@pytest.mark.parametrize("label, row, column", CELLS)
def test_button_position(app, label, row, column):
    info = app.buttons[label].grid_info()
    first, span = info["column"], info["columnspan"]
    assert info["row"] == row + 1  # строка 0 занята дисплеем
    assert first <= column < first + span


def test_zero_button_is_double_width(app):
    assert app.buttons["0"].grid_info()["columnspan"] == 2


# дальше проверяется, как окно на самом деле отрисовалось на экране

@pytest.mark.parametrize("label", LABELS)
def test_button_is_visible(shown_app, label):
    assert shown_app.buttons[label].winfo_viewable()


def test_display_is_visible(shown_app):
    assert shown_app.window.display.winfo_viewable()


def test_display_is_above_buttons(shown_app):
    display = shown_app.window.display
    display_bottom = display.winfo_y() + display.winfo_height()
    assert all(button.winfo_y() >= display_bottom for button in shown_app.buttons.values())


def test_display_is_as_wide_as_button_rows(shown_app):
    row = [shown_app.buttons[label] for label in LAYOUT[0]]
    row_width = row[-1].winfo_x() + row[-1].winfo_width() - row[0].winfo_x()
    # у дисплея отступ по бокам 5px, у кнопок 2px
    assert shown_app.window.display.winfo_width() == row_width - 2 * (5 - 2)


def test_buttons_go_left_to_right_and_top_to_bottom(shown_app):
    buttons = shown_app.buttons
    for labels in LAYOUT:
        xs = [buttons[label].winfo_x() for label in dict.fromkeys(labels)]
        assert xs == sorted(xs)
    ys = [buttons[labels[0]].winfo_y() for labels in LAYOUT]
    assert ys == sorted(set(ys))


def test_zero_button_is_wider_than_others(shown_app):
    buttons = shown_app.buttons
    assert buttons["0"].winfo_width() > 1.5 * buttons["1"].winfo_width()


def test_error_is_written_in_small_font(app):
    app.click("2", "+", "=")
    assert app.window.display.cget("font") == "Arial 12"


def test_font_is_back_to_normal_after_error(app):
    app.click("2", "+", "=", "5")
    assert app.window.display.cget("font") == "Arial 24"


@pytest.mark.parametrize("pressed", [
    ["√", "-", "4", ")", "="],  # самое длинное сообщение
    ["1", "÷", "0", "="],
    [*"1234567890" * 3],  # длинный ввод
])
def test_window_size_does_not_change(shown_app, pressed):
    window = shown_app.window
    size = (window.winfo_width(), window.winfo_height())
    shown_app.click(*pressed)
    assert (window.winfo_width(), window.winfo_height()) == size
