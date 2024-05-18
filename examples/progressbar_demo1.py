from pyguiadapter import GUIAdapter
from pyguiadapter.progressbar_config import ProgressBarConfig


def progressbar_demo1() -> int:
    pass


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    progressbar_config = ProgressBarConfig(
        min_value=0,
        max_value=1000,
        inverted_appearance=False,
        show_progress_text=True,
        progress_text_centered=True,
        progress_text_format="task %v in task %m",
        show_progressbar_info=False,
    )
    gui_adapter.add(
        progressbar_demo1,
        enable_progressbar=True,
        progressbar_config=progressbar_config,
    )
    gui_adapter.run()
