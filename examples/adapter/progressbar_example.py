import time

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter import uprogress
from pyguiadapter.adapter.ucontext import is_function_cancelled, uprint


def progressbar_example(target: int = 100, delay: float = 0.5):
    uprogress.show_progressbar(0, 100, message_visible=True)
    for i in range(target):
        if is_function_cancelled():
            uprint("Cancelled!")
            break
        uprint(f"[info] {i}")
        uprogress.update_progress(i, info=f"progress: <b>{i}%</b>")
        time.sleep(delay)
    uprogress.hide_progressbar()


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(progressbar_example, cancelable=True)
    adapter.run()
