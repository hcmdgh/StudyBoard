import win32api
from datetime import datetime


def _show_msgbox(*, title: str, text: str):
    win32api.MessageBox(0, text, title, 4096)


def notify_duration(duration: int):
    _show_msgbox(
        title="离骚",
        text=f"亦余心之所善兮，虽 {duration} 死其犹未悔。",
    )


_log_fp = open("./error.log", "a", encoding="utf-8")


def print_plus(msg: str):
    msg = f"[{datetime.now()}] {msg}"
    print(msg)
    print(msg, file=_log_fp, flush=True)
