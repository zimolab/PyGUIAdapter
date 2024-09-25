import ast
import dataclasses
import hashlib
import inspect
import os.path
import re
import string
import traceback
import warnings
from io import StringIO
from typing import Literal, List, Set, Tuple, Any, Union, Type, Optional

import qtawesome as qta
from qtpy import QT_VERSION, compat
from qtpy.QtCore import QUrl, Qt, QSize
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
    title: Optional[str] = None
    icon: Union[int, QPixmap, None] = None
    detailed_text: Optional[str] = None
    informative_text: Optional[str] = None
    text_format: Optional[TextFormat] = None
    buttons: Union[StandardButton, StandardButtons, int, None] = None
    default_button: Optional[StandardButton] = None
    escape_button: Optional[StandardButton] = None

    def create_messagebox(self, parent: Optional[QWidget]) -> QMessageBox:
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
def get_icon(src: IconType, *args, **kwargs) -> Optional[QIcon]:
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
) -> Union[int, StandardButton]:
    return QMessageBox.warning(parent, title, message)


def show_critical_message(
    parent: QWidget,
    message: str,
    title: str = "Critical",
) -> Union[int, StandardButton]:
    return QMessageBox.critical(parent, title, message)


def show_info_message(
    parent: QWidget,
    message: str,
    title: str = "Information",
) -> Union[int, StandardButton]:
    return QMessageBox.information(parent, title, message)


def show_question_message(
    parent: QWidget,
    message: str,
    title: str = "Question",
    buttons: Union[int, StandardButton, StandardButtons, None] = None,
) -> Union[int, StandardButton]:
    if buttons is None:
        return QMessageBox.question(parent, title, message)
    return QMessageBox.question(parent, title, message, buttons)


def show_exception_message(
    parent: Optional[QWidget],
    exception: Exception,
    message: str = "",
    title: str = "Error",
    detail: bool = True,
    show_error_type: bool = True,
    **kwargs,
) -> Union[int, StandardButton]:
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


def _marks(marks: Union[str, List[str], Tuple[str], Set[str]]) -> Set[str]:
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
    start_marks: Union[str, List[str], Tuple[str], Set[str]],
    end_marks: Union[str, List[str], Tuple[str], Set[str]],
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
    start_marks: Union[str, List[str], Tuple[str], Set[str]],
    end_marks: Union[str, List[str], Tuple[str], Set[str]],
) -> Optional[str]:
    pattern = _block_pattern(start_marks, end_marks)
    result = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.UNICODE)
    if result:
        return result.group(2)
    return None


def remove_text_block(
    text: str,
    start_marks: Union[str, List[str], Tuple[str], Set[str]],
    end_marks: Union[str, List[str], Tuple[str], Set[str]],
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
    parent: Optional[QWidget] = None,
    title: str = "Open Directory",
    start_dir: str = "",
) -> str:
    return compat.getexistingdirectory(parent, title, start_dir)
    # return QFileDialog.getExistingDirectory(parent, title, start_dir)


def get_existing_directory_url(
    parent: Optional[QWidget] = None,
    title: str = "Open Directory URL",
    start_dir: Optional[QUrl] = None,
    supported_schemes: Optional[List[str]] = None,
) -> Optional[QUrl]:
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
    parent: Optional[QWidget] = None,
    title: str = "Open File",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    # filename, _ = QFileDialog.getOpenFileName(parent, title, start_dir, filters)
    filename, _ = compat.getopenfilename(parent, title, start_dir, filters)
    return filename or None


def get_open_files(
    parent: Optional[QWidget] = None,
    title: str = "Open Files",
    start_dir: str = "",
    filters: str = "",
) -> Optional[List[str]]:
    # filenames, _ = QFileDialog.getOpenFileNames(parent, title, start_dir, filters)
    filenames, _ = compat.getopenfilenames(parent, title, start_dir, filters)
    return filenames or None


def get_save_file(
    parent: Optional[QWidget] = None,
    title: str = "Save File",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    # filename, _ = QFileDialog.getSaveFileName(parent, title, start_dir, filters)
    filename, _ = compat.getsavefilename(parent, title, start_dir, filters)
    return filename or None


def compare_qt_version(ver: Optional[str]) -> int:
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
    error: Exception, limit: Optional[int] = None, complete_msg: bool = True
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


def fingerprint(text: str) -> Optional[str]:
    if not text:
        return None
    md5 = hashlib.md5()
    md5.update(text.encode("utf-8"))
    return md5.hexdigest()


def get_size(size: Union[int, Tuple[int, int], QSize]) -> Optional[QSize]:
    if size is None:
        return None
    if isinstance(size, int):
        return QSize(size, size)
    if isinstance(size, tuple):
        assert len(size) == 2
        return QSize(*size)
    if isinstance(size, QSize):
        return size
    warnings.warn(f"invalid size type: {type(size)}")
    return None


def get_object_filename(obj: Any) -> Optional[str]:
    return inspect.getsourcefile(obj)


def get_object_sourcecode(obj: Any) -> Optional[str]:
    return inspect.getsource(obj)


def get_type_args(raw: str) -> list:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        content = raw[1:-1].strip()
    elif raw.startswith("(") and raw.endswith(")"):
        content = raw[1:-1].strip()
    else:
        content = None

    if content is None:
        return raw.split(",")

    content = "[" + content + "]"
    try:
        args = ast.literal_eval(content)
    except Exception as e:
        warnings.warn(f"unable to parse type args '{raw}': {e}")
        return []
    return args


def is_subclass_of(cls: Any, base_cls: Any):
    if not inspect.isclass(cls) or not inspect.isclass(base_cls):
        return False
    return issubclass(cls, base_cls)


def convert_color(
    c: QColor,
    return_type: Literal["tuple", "str", "QColor"],
    alpha_channel: bool = True,
) -> Union[Tuple[int, int, int, int], Tuple[int, int, int], str, QColor]:
    assert isinstance(c, QColor)
    if return_type == "QColor":
        return c

    if return_type == "tuple":
        if alpha_channel:
            return c.red(), c.green(), c.blue(), c.alpha()
        else:
            return c.red(), c.green(), c.blue()
    if return_type == "str":
        if alpha_channel:
            return f"#{c.red():02x}{c.green():02x}{c.blue():02x}{c.alpha():02x}"
        else:
            return f"#{c.red():02x}{c.green():02x}{c.blue():02x}"

    raise ValueError(f"invalid return_type: {return_type}")


# noinspection SpellCheckingInspection
def to_qcolor(color: Union[str, tuple, list, QColor]) -> QColor:
    if isinstance(color, QColor):
        return color
    if isinstance(color, (list, tuple)):
        if len(color) < 3:
            raise ValueError(f"invalid color tuple: {color}")
        c = QColor()
        c.setRgb(*color)
        return c
    if isinstance(color, str):
        return QColor(color)

    raise ValueError(f"invalid color type: {type(color)}")
