import subprocess
import sys
from pathlib import Path

from calculator import main as app_main
from calculator.ui.main_window import MainWindow

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_main_opens_calculator_window(app, monkeypatch):
    # фикстура app нужна только чтобы тест пропускался там, где окно не открыть
    windows = []
    monkeypatch.setattr(MainWindow, "mainloop", lambda window: windows.append(window))

    app_main.main()

    assert len(windows) == 1
    assert windows[0].title() == "Калькулятор"
    windows[0].destroy()


def test_app_starts_from_command_line(app):
    # python -m calculator.main не должен падать при запуске; живой процесс через 3 секунды —
    # значит, окно открылось и ждёт действий пользователя
    with subprocess.Popen(
        [sys.executable, "-m", "calculator.main"],
        cwd=PROJECT_ROOT,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            return
        raise AssertionError(f"приложение закрылось с кодом {process.returncode}:\n{process.stderr.read()}")
