from qtpy.QtWidgets import QAction

from pyguiadapter.action import ActionConfig
from pyguiadapter.adapter import GUIAdapter, utoast
from pyguiadapter.extend_types import text_t
from pyguiadapter.toast import ToastConfig
from pyguiadapter.toolbar import ToolBarConfig
from pyguiadapter.windows.fnexec import FnExecuteWindow


def show_toast(win: FnExecuteWindow, action: QAction):
    win.show_toast("Paused!", duration=3000, clear=True)


def clear_toasts(win: FnExecuteWindow, action: QAction):
    win.clear_toasts()


action_toast = ActionConfig(
    text="Toast",
    icon="mdi.message-text-clock",
    tooltip="Show toast message",
    on_triggered=show_toast,
)

action_clear_toasts = ActionConfig(
    text="Clear toasts",
    icon="ei.remove-circle",
    tooltip="Clear all toasts",
    on_triggered=clear_toasts,
)


def toast_example(
    message: text_t = "Hello world!",
    duration: int = 3000,
    clear: bool = False,
    fade_out: int = 0,
):
    if not message:
        return
    fade_out = max(fade_out, 0)
    utoast.show_toast(message, duration, ToastConfig(fade_out=fade_out), clear)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        toast_example,
        window_toolbar=ToolBarConfig(actions=[action_toast, action_clear_toasts]),
    )
    adapter.run()
