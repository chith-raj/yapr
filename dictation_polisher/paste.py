from __future__ import annotations

import subprocess
import time
from typing import Any, Dict

import pyperclip


def paste_text(text: str, config: Dict[str, Any]) -> None:
    if not text:
        return
    if not config.get("enabled", True):
        print(text, flush=True)
        return

    previous = pyperclip.paste()
    pyperclip.copy(text)
    time.sleep(float(config.get("paste_delay_seconds", 0.1)))

    subprocess.run(
        [
            "osascript",
            "-e",
            'tell application "System Events" to keystroke "v" using command down',
        ],
        check=True,
    )

    if config.get("restore_clipboard", False):
        time.sleep(0.2)
        pyperclip.copy(previous)
