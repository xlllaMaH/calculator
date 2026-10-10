# ui/main_window.py
import tkinter as tk
from calculator.ui.buttons import BUTTONS
from calculator.ui.display import Display
from calculator.ui.input_handler import InputHandler
# клавиши клавиатуры, которые отличаются от ключей кнопок
KEY_MAP = {"*": "×", "/": "÷", "\r": "=", "\x08": "back", "\x1b": "C"}
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор")
        self.resizable(False, False)
        self.display = Display(self)
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        self.handler = InputHandler(self.display)

        for label, key, row, col, *span in BUTTONS:
            tk.Button(
            self,
            text=label,
            width=6,
            height=2,
            command=lambda k=key: self.handler.press(k),
            ).grid(
                row=row + 1,
                column=col,
                columnspan=span[0] if span else 1,
                sticky="nsew",
                padx=2,
                pady=2,
            )


        self.keys = {key for _, key, *_ in BUTTONS}
        self.bind("<Key>", self._on_key)

    def _on_key(self, event):
        key = KEY_MAP.get(event.char, event.char)
        if key in self.keys:
            self.handler.press(key)