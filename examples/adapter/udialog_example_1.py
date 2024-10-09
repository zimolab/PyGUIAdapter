from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter import udialog
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.extend_types import text_t
from pyguiadapter.utils import messagebox


def dialog_example(
    info_message: text_t,
    warning_message: text_t,
    error_message: text_t,
    question_message: text_t,
):
    if info_message:
        udialog.show_info_messagebox(
            text=info_message,
            title="Information",
            buttons=messagebox.Ok | messagebox.No,
            default_button=messagebox.Ok,
        )

    if warning_message:
        udialog.show_warning_messagebox(
            text=warning_message,
            title="Warning",
            buttons=messagebox.Ok | messagebox.No,
            default_button=messagebox.Ok,
        )

    if error_message:
        udialog.show_critical_messagebox(
            text=error_message,
            title="Error",
            buttons=messagebox.Ok | messagebox.No,
            default_button=messagebox.Ok,
        )

    if question_message:
        answer = udialog.show_question_messagebox(
            text=question_message,
            title="Question",
            buttons=messagebox.Yes | messagebox.No,
            default_button=messagebox.No,
        )
        if answer == messagebox.Yes:
            uprint("Your Choice: Yes")
            udialog.show_info_messagebox("You Choose Yes!", title="Answer")
        else:
            uprint("Your Choice: No")
            udialog.show_info_messagebox("You Choose No!", title="Answer")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(dialog_example)
    adapter.run()
