import tkinter as tk
import unittest
from types import SimpleNamespace

from calculator.evaluator import BINARY, FUNCTIONS
from calculator.ui.buttons import BUTTONS
from calculator.ui.display import Display, WIDTH
from calculator.ui.main_window import MainWindow, KEY_MAP

CONTROL_KEYS = {"=", "C", "back", "mc", "mr", "m+", "m-"}
BUTTON_KEYS = {key for _, key, *_ in BUTTONS}


class TestButtons(unittest.TestCase):

    def test_keys_are_unique(self):
        keys = [key for _, key, *_ in BUTTONS]
        self.assertEqual(len(keys), len(set(keys)))

    def test_keys_are_understood_by_evaluator(self):
        for key in BUTTON_KEYS - CONTROL_KEYS:
            with self.subTest(key=key):
                if key.endswith("(") and len(key) > 1:
                    self.assertIn(key[:-1], FUNCTIONS)
                elif key not in "0123456789.()":
                    self.assertIn(key, BINARY)

    def test_buttons_do_not_overlap(self):
        cells = set()
        for label, _, row, col, *span in BUTTONS:
            for c in range(col, col + (span[0] if span else 1)):
                with self.subTest(button=label):
                    self.assertIn(c, range(4))
                    self.assertNotIn((row, c), cells)
                cells.add((row, c))

    def test_key_map_targets_existing_buttons(self):
        for char, key in KEY_MAP.items():
            with self.subTest(char=char):
                self.assertIn(key, BUTTON_KEYS)


# Тестам ниже нужен экран. Без него (например, в CI без xvfb) они пропускаются.

class TestDisplay(unittest.TestCase):

    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"Tk недоступен: {error}")
        self.root.withdraw()
        self.display = Display(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_starts_with_zero(self):
        self.assertEqual(self.display.get(), "0")

    def test_set(self):
        self.display.set("12+3")
        self.assertEqual(self.display.get(), "12+3")

    def test_long_value_is_cut_from_the_left(self):
        value = "1234567890" * 2
        self.display.set(value)
        self.assertEqual(self.display.get(), "…" + value[-(WIDTH - 1):])
        self.assertEqual(len(self.display.get()), WIDTH)

    def test_value_of_max_width_is_not_cut(self):
        value = "9" * WIDTH
        self.display.set(value)
        self.assertEqual(self.display.get(), value)


class TestMainWindow(unittest.TestCase):

    def setUp(self):
        try:
            self.window = MainWindow()
        except tk.TclError as error:
            self.skipTest(f"Tk недоступен: {error}")
        self.window.withdraw()
        self.buttons = {
            widget["text"]: widget
            for widget in self.window.winfo_children()
            if isinstance(widget, tk.Button)
        }

    def tearDown(self):
        self.window.destroy()

    def click(self, *labels):
        for label in labels:
            self.buttons[label].invoke()
        return self.window.display.get()

    def type(self, chars):
        for char in chars:
            self.window._on_key(SimpleNamespace(char=char))
        return self.window.display.get()

    def test_title(self):
        self.assertEqual(self.window.title(), "Калькулятор")

    def test_not_resizable(self):
        self.assertEqual(self.window.resizable(), (0, 0))

    def test_all_buttons_created(self):
        self.assertEqual(set(self.buttons), {label for label, *_ in BUTTONS})

    def test_buttons_placed_below_display(self):
        for label, _, row, col, *_ in BUTTONS:
            with self.subTest(button=label):
                info = self.buttons[label].grid_info()
                self.assertEqual((info["row"], info["column"]), (row + 1, col))

    def test_click_buttons(self):
        self.assertEqual(self.click("9", "÷", "4", "="), "2.25")
        self.assertEqual(self.click("C", "√", "1", "6", ")", "^", "2", "="), "16")

    def test_click_error(self):
        self.assertEqual(self.click("1", "÷", "0", "="), "Деление на ноль")

    def test_key_binding(self):
        self.assertIn("<Key>", self.window.bind())

    def test_keyboard(self):
        self.assertEqual(self.type("12*3\r"), "36")
        self.assertEqual(self.type("8/2\r"), "4")

    def test_keyboard_control_keys(self):
        self.assertEqual(self.type("123\x08"), "12")
        self.assertEqual(self.type("\x1b"), "0")

    def test_unknown_key_is_ignored(self):
        self.type("1q@")
        self.assertEqual(self.window.handler.expression, "1")


if __name__ == "__main__":
    unittest.main()
