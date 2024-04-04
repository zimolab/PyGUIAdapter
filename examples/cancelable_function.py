from threading import Event
import time

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.ulogging import debug


def cancelable_function(
    delay_time: int = 1, iterations: int = 100, cancel_event: Event = None
):
    """
    This demo shows how to make a function cancelable and how to response the cancel request from UI

    :param delay_time:
    :param iterations:
    :param cancel_event:
    :return:
    """
    for i in range(iterations):
        if cancel_event and cancel_event.is_set():
            debug("cancel requested!")
            return
        debug(f"iteration: {i}")
        if delay_time > 0:
            time.sleep(delay_time)


if __name__ == "__main__":
    gui_adapter = GUIAdapter()
    gui_adapter.add(cancelable_function, cancelable=True)
    gui_adapter.run()
