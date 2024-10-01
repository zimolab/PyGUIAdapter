from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter import udialog
from pyguiadapter.adapter.ucontext import uprint
from pyguiadapter.extend_types import text_t


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
            buttons=udialog.QMessageBox.Ok | udialog.QMessageBox.No,
            default_button=udialog.QMessageBox.Ok,
        )

    if warning_message:
        udialog.show_warning_messagebox(
            text=warning_message,
            title="Warning",
            buttons=udialog.QMessageBox.Ok | udialog.QMessageBox.No,
            default_button=udialog.QMessageBox.Ok,
        )

    if error_message:
        udialog.show_critical_messagebox(
            text=error_message,
            title="Error",
            buttons=udialog.QMessageBox.Ok | udialog.QMessageBox.No,
            default_button=udialog.QMessageBox.Ok,
        )

    if question_message:
        answer = udialog.show_question_messagebox(
            text=question_message,
            title="Question",
            buttons=udialog.QMessageBox.Yes | udialog.QMessageBox.No,
            default_button=udialog.QMessageBox.No,
        )
        if answer == udialog.QMessageBox.Yes:
            uprint("Your Choice: Yes")
            udialog.show_info_messagebox("You Choose Yes!", title="Answer")
        else:
            uprint("Your Choice: No")
            udialog.show_info_messagebox("You Choose No!", title="Answer")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(dialog_example)
    adapter.run()
