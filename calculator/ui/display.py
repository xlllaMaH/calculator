import tkinter as tk
import tkinter.font as tkfont

WIDTH = 15
FONT = ("Arial", 24)
ERROR_FONT = ("Arial", 12)


class Display(tk.Label):

    def __init__(self, master):
        self._text = tk.StringVar(master=master, value="0")
        self._pixel = tk.PhotoImage(master=master, width=1, height=1)
        font = tkfont.Font(root=master, font=FONT)
        width = font.measure("0") * WIDTH
        super().__init__(
            master,
            textvariable=self._text,
            image=self._pixel,
            compound="center",
            anchor="e",
            justify="right",
            width=width,
            height=font.metrics("linespace"),
            wraplength=width,
            font=FONT,
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
        self.configure(font=FONT)
        self._text.set(value)

    def show_error(self, message):
        """Показывает сообщение целиком: мелким шрифтом и с переносом строк."""
        self.configure(font=ERROR_FONT)
        self._text.set(message)
