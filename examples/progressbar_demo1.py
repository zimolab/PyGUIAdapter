import time
from pyguiadapter import GUIAdapter
from pyguiadapter.progressbar_config import ProgressBarConfig
from pyguiadapter.interact.uprint import (
    update_progress,
    update_progressbar_config,
    uprint,
)


def progressbar_demo1(min_value: int, max_value: int = 10, delay: float = 1.0):
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


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    progressbar_config = ProgressBarConfig(
        min_value=0,
        max_value=1000,
        inverted_appearance=False,
        show_progress_text=True,
        progress_text_centered=True,
        progress_text_format="%v / %m (%p%)",
        show_progressbar_info=False,
    )
    gui_adapter.add(
        progressbar_demo1,
        enable_progressbar=True,
        progressbar_config=progressbar_config,
    )
    gui_adapter.run()
