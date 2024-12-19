import time

from pyguiadapter.adapter import GUIAdapter, udialog
from pyguiadapter.adapter import uprogress
from pyguiadapter.adapter.ucontext import is_function_cancelled
from pyguiadapter.adapter.uoutput import uprint


def progress_dialog_example(total: int = 100, delay: float = 0.5):
    """
    An example for **progress dialog** features

    @param total: how many task will be processed
    @param delay: how much time will be consumed per task
    @return:
    """
    cancelled = False
    task_processed = 0
    # use this function to show a progress dialog
    uprogress.show_progress_dialog(0, total, message_visible=True, info_visible=True)
    for i in range(total):
        if is_function_cancelled():
            uprint("Cancelled!")
            cancelled = True
            break
        task_processed = i + 1
        uprint(f"[Processed] {task_processed}")
        # use this function to update the progressbar and info message in the progress dialog
        uprogress.update_progress_dialog(
            task_processed, info=f"[{task_processed}/{total}] please wait..."
        )
        time.sleep(delay)
    if cancelled:
        udialog.show_warning_messagebox(
            f"{task_processed} task(s) processed!", title="Cancelled"
        )
    else:
        udialog.show_info_messagebox(
            f"{task_processed} task(s) processed!", title="Completed"
        )
    # use this function to dismiss the progress dialog after the task is done
    uprogress.dismiss_progress_dialog()


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(progress_dialog_example, cancelable=True)
    adapter.run()
