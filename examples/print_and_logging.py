"""
In PyGUIAdapter, we use uprint and ulogging to show the messages in the output window
"""

from pyguiadapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint
from pyguiadapter.interact import ulogging


def print_logging_demo(your_name: str):
    """Use uprint and ulogging to print message to the output window"""
    ulogging.enable_timestamp(True)

    uprint(f"hello, {your_name}! Let me show your a Chinese poem!")

    poem_text = """
    <h2 style="color:red">静夜思</h2>
    <h3 style="font-style:italic">李白</h3>
    <p>床前明月光，</p>
    <p>疑似地上霜。</p>
    <p>举头望明月，</p>
    <p>低头思故乡。</p>
    <br>
    """.strip()
    uprint(poem_text, html=True)

    ulogging.info(f"hello world!")
    ulogging.debug(f"hello world!")
    ulogging.warning(f"hello world!")
    ulogging.critical(f"hello world!")
    uprint("hello world!")


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(print_logging_demo)
    gui_adapter.run()
