import os
import tkinter as tk

import pytest

from calculator.operations.memory import m_clear
from calculator.ui.main_window import MainWindow


def create_window():
    """Создаёт окно калькулятора. Без экрана тест пропускается, а в CI падает."""
    try:
        return MainWindow()
    except tk.TclError as error:
        if os.environ.get("CI"):
            raise
        pytest.skip(f"нет экрана для окна Tk: {error}")


class App:
    """Настоящее окно калькулятора, с которым тест работает как пользователь."""

    def __init__(self, window):
        self.window = window
        self.buttons = {
            widget["text"]: widget
            for widget in window.winfo_children()
            if isinstance(widget, tk.Button)
        }

    def screen(self):
        """Текст, который сейчас виден на дисплее."""
        display = self.window.display
        return display.getvar(display.cget("textvariable"))

    def click(self, *labels):
        """Нажимает кнопки по подписям на них и возвращает текст на дисплее."""
        for label in labels:
            self.buttons[label].invoke()
        self.window.update()
        return self.screen()

    def press_keys(self, *keysyms):
        """Нажимает клавиши клавиатуры (имена клавиш Tk) и возвращает текст на дисплее."""
        for keysym in keysyms:
            self.window.event_generate("<KeyPress>", keysym=keysym)
        self.window.update()
        return self.screen()


@pytest.fixture(autouse=True)
def clean_memory():
    # память калькулятора — глобальное состояние, тесты не должны влиять друг на друга
    m_clear()
    yield
    m_clear()


@pytest.fixture
def app():
    """Окно калькулятора, скрытое с экрана: для нажатия кнопок показывать его не нужно."""
    window = create_window()
    window.withdraw()
    window.update()
    yield App(window)
    window.destroy()


@pytest.fixture
def shown_app():
    """Окно на экране и с фокусом: так оно получает события клавиатуры и отрисовывается."""
    window = create_window()
    window.update()
    window.focus_force()
    window.update()
    yield App(window)
    window.destroy()
