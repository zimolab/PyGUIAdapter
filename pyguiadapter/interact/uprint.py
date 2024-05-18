import os.path

from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

from pyguiadapter.progressbar_config import ProgressBarConfig


class UPrint(QObject):
    printed = pyqtSignal(str, bool)
    progress_updated = pyqtSignal(int, str)
    progressbar_config_updated = pyqtSignal(ProgressBarConfig)
    progressbar_visibility_updated = pyqtSignal(bool)

    def print(self, *args, sep=" ", end="\n", html: bool = False):
        text = sep.join([str(arg) for arg in args]) + end
        # noinspection PyUnresolvedReferences
        self.printed.emit(text, html)

    def update_progress(
        self,
        current_value: int,
        progress_info: Optional[str] = None,
    ):
        # noinspection PyUnresolvedReferences
        self.progress_updated.emit(current_value, progress_info)

    def hide_progressbar(self):
        # noinspection PyUnresolvedReferences
        self.progressbar_visibility_updated.emit(False)

    def show_progressbar(self):
        # noinspection PyUnresolvedReferences
        self.progressbar_visibility_updated.emit(True)

    def update_progressbar_config(
        self,
        min_value: int = 0,
        max_value: int = 100,
        inverted_appearance: bool = False,
        show_progressbar_info: bool = False,
        show_progress_text: bool = True,
        progress_text_centered: bool = True,
        progress_text_format: str = "%p%",
    ):
        new_config = ProgressBarConfig(
            min_value=min_value,
            max_value=max_value,
            inverted_appearance=inverted_appearance,
            show_progressbar_info=show_progressbar_info,
            show_progress_text=show_progress_text,
            progress_text_centered=progress_text_centered,
            progress_text_format=progress_text_format,
        )
        # noinspection PyUnresolvedReferences
        self.progressbar_config_updated.emit(new_config)


__uprint = UPrint()


def set_print_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.printed.connect(func)


def set_update_progress_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.progress_updated.connect(func)


def set_update_progressbar_config_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.progressbar_config_updated.connect(func)


def set_update_progressbar_visibility_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.progressbar_visibility_updated.connect(func)


def remove_print_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.printed.disconnect(func)


def remove_update_progress_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.progress_updated.disconnect(func)


def remove_update_progressbar_config_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.progressbar_config_updated.disconnect(func)


def remove_update_progressbar_visibility_destination(func: callable):
    # noinspection PyUnresolvedReferences
    __uprint.progressbar_visibility_updated.disconnect(func)


def uprint(*args, sep=" ", end="\n", html: bool = False):
    __uprint.print(*args, sep=sep, end=end, html=html)


def uprint_image(image_path: str, alt_text: str = "", blank_lines_around: bool = False):
    if blank_lines_around:
        outer_tag = "<br>{}<br>"
    else:
        outer_tag = "{}"

    img_tag = f"<img src='{os.path.abspath(image_path)}' alt='{alt_text}' />"

    uprint(outer_tag.format(img_tag), html=True)


def update_progress(current_value: int, progress_info: Optional[str] = None):
    __uprint.update_progress(current_value, progress_info)


def update_progressbar_config(
    min_value: int = 0,
    max_value: int = 100,
    inverted_appearance: bool = False,
    show_progressbar_info: bool = False,
    show_progress_text: bool = True,
    progress_text_centered: bool = True,
    progress_text_format: str = "%p%",
):
    __uprint.update_progressbar_config(
        max_value=max_value,
        min_value=min_value,
        inverted_appearance=inverted_appearance,
        show_progressbar_info=show_progressbar_info,
        show_progress_text=show_progress_text,
        progress_text_centered=progress_text_centered,
        progress_text_format=progress_text_format,
    )


def hide_progressbar():
    __uprint.hide_progressbar()


def show_progressbar():
    __uprint.show_progressbar()
