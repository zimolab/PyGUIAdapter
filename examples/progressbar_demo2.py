import time

from pyguiadapter import GUIAdapter
from pyguiadapter.interact.uprint import (
    update_progress,
    update_progressbar_config,
    show_progressbar,
    hide_progressbar,
    uprint,
)


def progressbar_demo2(min_value: int, max_value: int = 10, delay: float = 1.0):
    show_progressbar()
    update_progressbar_config(
        min_value=min_value,
        max_value=max_value,
        progress_text_format="%v/%m (%p%)",
        show_progressbar_info=True,
    )
    for i in range(min_value, max_value + 1):
        uprint(f"processing: {i}")
        update_progress(
            i, progress_info=f"processing item {i}... \nthis may take some time"
        )
        time.sleep(delay)
    uprint("process done")
    # reset progress manually
    update_progress(min_value, progress_info="")
    hide_progressbar()


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(progressbar_demo2)
    gui_adapter.run()
