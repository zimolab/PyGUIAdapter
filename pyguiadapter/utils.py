from __future__ import annotations

import dataclasses
import os.path
import re
import string
import traceback
from io import StringIO
from typing import Literal, List, Set, Tuple, Any, Union, Type

import qtawesome as qta
from qtpy import QT_VERSION
from qtpy.QtCore import QUrl, Qt
from qtpy.QtGui import QIcon, QPixmap, QTextCursor, QTextOption, QColor
from qtpy.QtWidgets import QTextBrowser, QWidget, QMessageBox, QFrame, QFileDialog

StandardButton: Type[QMessageBox.StandardButton] = QMessageBox.StandardButton
StandardButtons: Type[QMessageBox.StandardButtons] = QMessageBox.StandardButtons
TextFormat = Qt.TextFormat

# noinspection SpellCheckingInspection
TEXTBROWSER_CSS = """
QTextEdit{
    background-color: ${bg_color};
    color: ${text_color};
    font-family: ${font_family};
    font-size: ${font_size}pt;
}
QScrollBar::vertical{
    background:transparent;
    width: 6px;
    margin: 0px;
 }
QScrollBar::handle:vertical{
    background-color:rgb(158,158,158);
    border: none;
    border-radius: 3px;
 }
QScrollBar::handle:vertical:pressed{
    background:#EC693C;
}
QScrollBar::sub-line:vertical{
    border:none;
}
QScrollBar::add-line:vertical{
    border:none;
}
QScrollBar::sub-page:vertical{
    border:none;
}
QScrollBar::add-page:vertical{
    border:none;
}
"""

IconType = Union[str, Tuple[str, Union[list, dict]], QIcon, QPixmap, type(None)]


@dataclasses.dataclass
class MessageBoxConfig(object):
    text: str
    title: str | None = None
    icon: int | QPixmap | None = None
    detailed_text: str | None = None
    informative_text: str | None = None
    text_format: TextFormat | None = None
    buttons: StandardButton | StandardButtons | None = None
    default_button: StandardButton | None = None
    escape_button: StandardButton | None = None

    def create_messagebox(self, parent: QWidget | None) -> QMessageBox:
        # noinspection SpellCheckingInspection,PyArgumentList
        msgbox = QMessageBox(parent)
        msgbox.setText(self.text)

        if self.title:
            msgbox.setWindowTitle(self.title)

        if self.icon is not None:
            msgbox.setIcon(self.icon)

        if isinstance(self.icon, QPixmap):
            msgbox.setIconPixmap(self.icon)

        if self.informative_text:
            msgbox.setInformativeText(self.informative_text)

        if self.detailed_text:
            msgbox.setDetailedText(self.detailed_text)

        if self.text_format is not None:
            msgbox.setTextFormat(self.text_format)

        if self.buttons is not None:
            msgbox.setStandardButtons(self.buttons)

        if self.default_button is not None:
            msgbox.setDefaultButton(self.default_button)

        if self.escape_button is not None:
            msgbox.setEscapeButton(self.escape_button)

        return msgbox


# noinspection PyArgumentList
def get_icon(src: IconType, *args, **kwargs) -> QIcon | None:
    if src is None:
        return None
    if isinstance(src, QIcon):
        return src
    if isinstance(src, QPixmap):
        return QIcon(src)
    if isinstance(src, str):
        if os.path.isfile(src) or src.startswith(":/"):
            return QIcon(src)
        return qta.icon(src, *args, **kwargs)
    if isinstance(src, tuple):
        assert len(src) >= 2
        assert isinstance(src[0], str) and isinstance(src[1], (dict, list))
        if isinstance(src[1], dict):
            return qta.icon(src[0], **src[1])
        else:
            return qta.icon(src[0], *src[1])
    else:
        raise ValueError(f"invalid icon type: {type(src)}")


# noinspection SpellCheckingInspection
def set_textbrowser_content(
    textbrowser: QTextBrowser,
    content: str,
    content_format: Literal["markdown", "html", "plaintext"] = "markdown",
):
    content_format = content_format.lower()
    if content_format == "markdown":
        textbrowser.setMarkdown(content)
    elif content_format == "html":
        textbrowser.setHtml(content)
    elif content_format == "plaintext":
        textbrowser.setPlainText("")
        textbrowser.append(content)
    else:
        raise ValueError(f"invalid content format: {content_format}")

    cursor = textbrowser.textCursor()
    cursor.movePosition(
        QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor
    )
    textbrowser.setTextCursor(cursor)


# noinspection SpellCheckingInspection
def get_textbrowser_stylesheet(
    bg_color: str, text_color: str, font_size: int, font_family: str
):
    css = string.Template(TEXTBROWSER_CSS).substitute(
        bg_color=bg_color,
        text_color=text_color,
        font_size=font_size,
        font_family=font_family,
    )
    return css.strip()


# noinspection SpellCheckingInspection
def set_textbrowser_wrap_mode(
    textbrowser: QTextBrowser,
    line_wrap_mode: Literal[
        "no_wrap", "widget_width", "fixed_pixel_width", "fixed_column_width"
    ] = "widget_width",
    word_wrap_mode: Literal[
        "no_wrap",
        "word_wrap",
        "manual_wrap",
        "wrap_anywhere",
        "wrap_at_word_boundary_or_anywhere",
    ] = "no_wrap",
    fixed_line_wrap_width: int = 80,
):
    if line_wrap_mode == "no_wrap":
        textbrowser.setLineWrapMode(QTextBrowser.LineWrapMode.NoWrap)
    elif line_wrap_mode == "widget_width":
        textbrowser.setLineWrapMode(QTextBrowser.LineWrapMode.WidgetWidth)
    elif line_wrap_mode == "fixed_pixel_width":
        textbrowser.setLineWrapMode(QTextBrowser.LineWrapMode.FixedPixelWidth)
        textbrowser.setLineWrapColumnOrWidth(fixed_line_wrap_width)
    elif line_wrap_mode == "fixed_column_width":
        textbrowser.setLineWrapMode(QTextBrowser.LineWrapMode.FixedColumnWidth)
        textbrowser.setLineWrapColumnOrWidth(fixed_line_wrap_width)
    else:
        raise ValueError(f"invalid line wrap mode: {line_wrap_mode}")

    if word_wrap_mode == "no_wrap":
        textbrowser.setWordWrapMode(QTextOption.NoWrap)
    elif word_wrap_mode == "word_wrap":
        textbrowser.setWordWrapMode(QTextOption.WordWrap)
    elif word_wrap_mode == "manual_wrap":
        textbrowser.setWordWrapMode(QTextOption.ManualWrap)
    elif word_wrap_mode == "wrap_anywhere":
        textbrowser.setWordWrapMode(QTextOption.WrapAnywhere)
    elif word_wrap_mode == "wrap_at_word_boundary_or_anywhere":
        textbrowser.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
    else:
        raise ValueError(f"invalid word wrap mode: {word_wrap_mode}")


def show_warning_message(
    parent: QWidget,
    message: str,
    title: str = "Warning",
) -> int | StandardButton:
    return QMessageBox.warning(parent, title, message)


def show_critical_message(
    parent: QWidget,
    message: str,
    title: str = "Critical",
) -> int | StandardButton:
    return QMessageBox.critical(parent, title, message)


def show_info_message(
    parent: QWidget,
    message: str,
    title: str = "Information",
) -> int | StandardButton:
    return QMessageBox.information(parent, title, message)


def show_question_message(
    parent: QWidget,
    message: str,
    title: str = "Question",
    buttons: int | StandardButton | StandardButtons | None = None,
) -> int | StandardButton:
    if buttons is None:
        return QMessageBox.question(parent, title, message)
    return QMessageBox.question(parent, title, message, buttons)


def show_exception_message(
    parent: QWidget | None,
    exception: Exception,
    message: str = "",
    title: str = "Error",
    detail: bool = True,
    show_error_type: bool = True,
    **kwargs,
) -> int | StandardButton:
    traceback.print_exc()
    if not detail:
        detail_msg = None
    else:
        detail_msg = get_traceback(exception)

    if show_error_type:
        error_msg = f"{type(exception).__name__}: {exception}"
    else:
        error_msg = str(exception)

    if message:
        error_msg = f"{message}{error_msg}"
    msgbox = MessageBoxConfig(
        title=title,
        text=error_msg,
        icon=QMessageBox.Critical,
        detailed_text=detail_msg,
        **kwargs,
    ).create_messagebox(parent)
    return msgbox.exec_()


# noinspection SpellCheckingInspection
def hline(parent: QWidget) -> QFrame:
    line = QFrame(parent)
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line


def _marks(marks: str | List[str] | Tuple[str] | Set[str]) -> Set[str]:
    if not isinstance(marks, (list, tuple, set, str)):
        raise TypeError(f"unsupported types for marks: {type(marks)}")
    if isinstance(marks, str):
        if marks.strip() == "":
            raise ValueError("marks must be a non-empty string")
        return {marks}

    if len(marks) <= 0:
        raise ValueError("at least one mark must be provided")

    tmp = set()
    for mark in marks:
        if not isinstance(mark, str):
            raise TypeError(f"a mark must be a string: {type(mark)}")
        if mark.strip() == "":
            raise ValueError("an empty-string mark found")
        tmp.add(mark)
    return tmp


def _block_pattern(
    start_marks: str | List[str] | Tuple[str] | Set[str],
    end_marks: str | List[str] | Tuple[str] | Set[str],
) -> str:
    start_marks = _marks(start_marks)
    end_marks = _marks(end_marks)

    start_mark_choices = "|".join(start_marks)
    end_mark_choices = "|".join(end_marks)
    pattern = (
        rf"^(\s*(?:{start_mark_choices})\s*(.*\n.+)^\s*(?:{end_mark_choices})\s*\n)"
    )
    return pattern


def extract_text_block(
    text: str,
    start_marks: str | List[str] | Tuple[str] | Set[str],
    end_marks: str | List[str] | Tuple[str] | Set[str],
) -> str | None:
    pattern = _block_pattern(start_marks, end_marks)
    result = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.UNICODE)
    if result:
        return result.group(2)
    return None


def remove_text_block(
    text: str,
    start_marks: str | List[str] | Tuple[str] | Set[str],
    end_marks: str | List[str] | Tuple[str] | Set[str],
) -> str:
    pattern = _block_pattern(start_marks, end_marks)
    result = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.UNICODE)
    if not result:
        return text
    return re.sub(
        pattern, repl="", string=text, flags=re.MULTILINE | re.DOTALL | re.UNICODE
    )


def hashable(obj: Any) -> bool:
    try:
        hash(obj)
        return True
    except TypeError:
        return False


def read_text_file(text_file: str, encoding: str = "utf-8") -> str:
    with open(text_file, "r", encoding=encoding) as f:
        return f.read()


def write_text_file(text_file: str, content: str, encoding: str = "utf-8"):
    with open(text_file, "w", encoding=encoding) as f:
        f.write(content)


def get_existing_directory(
    parent: QWidget | None = None,
    title: str = "Open Directory",
    start_dir: str = "",
) -> str:
    return QFileDialog.getExistingDirectory(parent, title, start_dir)


def get_existing_directory_url(
    parent: QWidget | None = None,
    title: str = "Open Directory URL",
    start_dir: QUrl | None = None,
    supported_schemes: List[str] | None = None,
) -> QUrl | None:
    if start_dir is None:
        start_dir = QUrl()
    if not supported_schemes:
        url = QFileDialog.getExistingDirectoryUrl(
            parent,
            title,
            start_dir,
            QFileDialog.ShowDirsOnly,
        )
    else:
        url = QFileDialog.getExistingDirectoryUrl(
            parent,
            title,
            start_dir,
            QFileDialog.ShowDirsOnly,
            supportedSchemes=supported_schemes,
        )
    return url


def get_open_file(
    parent: QWidget | None = None,
    title: str = "Open File",
    start_dir: str = "",
    filters: str = "",
) -> str | None:
    filename, _ = QFileDialog.getOpenFileName(parent, title, start_dir, filters)
    return filename or None


def get_open_files(
    parent: QWidget | None = None,
    title: str = "Open Files",
    start_dir: str = "",
    filters: str = "",
) -> List[str] | None:
    filenames, _ = QFileDialog.getOpenFileNames(parent, title, start_dir, filters)
    return filenames or None


def get_save_file(
    parent: QWidget | None = None,
    title: str = "Save File",
    start_dir: str = "",
    filters: str = "",
) -> str | None:
    filename, _ = QFileDialog.getSaveFileName(parent, title, start_dir, filters)
    return filename or None


def compare_qt_version(ver: str | None) -> int:
    if not ver:
        return 1
    if not QT_VERSION:
        return -1
    cur_ver = tuple(map(int, QT_VERSION.split(".")))
    cmp_ver = tuple(map(int, ver.split(".")))
    return (cur_ver > cmp_ver) - (cur_ver < cmp_ver)


def unique_list(origin: List[Any]) -> List[Any]:
    added = set()
    bool_true_added = False
    bool_false_added = False
    ret = []
    for item in origin:
        if item is True:
            if not bool_true_added:
                ret.append(item)
                bool_true_added = True
        elif item is False:
            if not bool_false_added:
                ret.append(item)
                bool_false_added = True
        else:
            if item not in added:
                added.add(item)
                ret.append(item)
    return ret


def get_inverted_color(color: QColor) -> QColor:
    return QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())


def get_traceback(
    error: Exception, limit: int | None = None, complete_msg: bool = True
) -> str:
    assert isinstance(error, Exception)
    buffer = StringIO()
    if complete_msg:
        buffer.write("Traceback (most recent call last):\n")
    traceback.print_tb(error.__traceback__, limit=limit, file=buffer)
    if complete_msg:
        buffer.write(f"{type(error).__name__}: {error}")
    msg = buffer.getvalue()
    buffer.close()
    return msg
