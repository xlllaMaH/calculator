import tkinter as tk

WIDTH = 15


class Display(tk.Label):

    def __init__(self, master):
        self._text = tk.StringVar(master=master, value="0")
        super().__init__(
            master,
            textvariable=self._text,
            anchor="e",
            width=WIDTH,
            font=("Arial", 24),
            bg="white",
            relief="sunken",
            padx=10,
            pady=10,
        )

    def get(self):
        return self._text.get()

    def set(self, value):
        if len(value) > WIDTH:
            value = "…" + value[-(WIDTH - 1):]
        self._text.set(value)