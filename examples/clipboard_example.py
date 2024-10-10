import time

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.ucontext import uprint, is_function_cancelled
from pyguiadapter.adapter import uclipboard
from pyguiadapter.extend_types import text_t


def clipboard_example(text: text_t):
    uprint("selection support:", uclipboard.supports_selection())
    uprint("owns selection:", uclipboard.owns_selection())
    uprint("owns clipboard:", uclipboard.owns_clipboard())
    uprint("selection text:")
    uprint(uclipboard.get_selection_text())
    uprint("clipboard text:")
    uprint(uclipboard.get_text())
    uprint("set clipboard text...")
    uclipboard.set_text(text)
    uprint("clipboard text:")
    uprint(uclipboard.get_text())
    uprint("======================")
    # for i in range(1000):
    #     if is_function_cancelled():
    #         break
    #     uprint("hello world ", i)
    #     time.sleep(0.01)
    time.sleep(5)
    for i in range(10):
        uclipboard.set_text(f"hello world {i}")
        time.sleep(0.5)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(clipboard_example)
    adapter.run()
