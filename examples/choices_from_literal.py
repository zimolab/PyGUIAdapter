from pyguiadapter.adapter import GUIAdapter
from typing import Literal

def choices_from_literal(
    choice: Literal["audio", "video", "subtitles", "all"] = "all",
):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(choices_from_literal)
    adapter.run()
