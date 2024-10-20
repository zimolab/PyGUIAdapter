"""
@Time    : 2024/10/20
@Author  : zimolab
@File    : messagebox.py
@Project : PyGUIAdapter
@Desc    : 消息对话框相关的工具函数
"""

import dataclasses
from typing import Any, Literal, Tuple, Type, Optional, Union

from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtWidgets import (
    QWidget,
    QDialogButtonBox,
    QTextBrowser,
    QVBoxLayout,
    QMessageBox,
)

from ._core import get_traceback
from .dialog import BaseCustomDialog
from ._ui import IconType, get_icon
from .io import read_text_file

StandardButton: Type[QMessageBox.StandardButton] = QMessageBox.StandardButton
TextFormat = Qt.TextFormat

Yes = StandardButton.Yes
No = StandardButton.No
Ok = StandardButton.Ok
Cancel = StandardButton.Cancel
NoButton = QMessageBox.NoButton

DialogButton: Type[QDialogButtonBox.StandardButton] = QDialogButtonBox.StandardButton
DialogButtons = Union[DialogButton, int]
DialogButtonYes = DialogButton.Yes
DialogButtonNo = DialogButton.No
DialogButtonCancel = DialogButton.Cancel
DialogButtonOk = DialogButton.Ok
DialogNoButton = QDialogButtonBox.NoButton

MessageBoxIcon: Type[QMessageBox.Icon] = QMessageBox.Icon
InformationIcon = MessageBoxIcon.Information
WarningIcon = MessageBoxIcon.Warning
CriticalIcon = MessageBoxIcon.Critical
QuestionIcon = MessageBoxIcon.Question
NoIcon = MessageBoxIcon.NoIcon


#########Standard MessageBox#################
def show_warning_message(
    parent: QWidget,
    message: str,
    title: str = "Warning",
) -> Union[int, StandardButton]:
    """
    显示警告消息对话框。

    Args:
        parent: 父窗口
        message: 消息内容
        title: 对话框标题

    Returns:
        返回用户点击的按钮的按键值
    """
    return QMessageBox.warning(parent, title, message)


def show_critical_message(
    parent: QWidget,
    message: str,
    title: str = "Critical",
) -> Union[int, StandardButton]:
    """
    显示严重错误消息对话框。

    Args:
        parent: 父窗口
        message: 消息内容
        title:  对话框标题

    Returns:
        返回用户点击的按钮的按键值
    """
    return QMessageBox.critical(parent, title, message)


def show_info_message(
    parent: QWidget,
    message: str,
    title: str = "Information",
) -> Union[int, StandardButton]:
    """
    显示一般信息消息对话框。

    Args:
        parent: 父窗口
        message:  消息内容
        title:  对话框标题

    Returns:
        返回用户点击的按钮的按键值。
    """
    return QMessageBox.information(parent, title, message)


def show_question_message(
    parent: QWidget,
    message: str,
    title: str = "Question",
    buttons: Union[int, StandardButton, None] = None,
) -> Union[int, StandardButton]:
    """
    显示询问消息对话框。

    Args:
        parent: 父窗口
        message: 消息内容
        title: 对话框标题
        buttons: 对话框标准按钮

    Returns:
        返回用户点击的按钮的按键值
    """
    if buttons is None:
        return QMessageBox.question(parent, title, message)
    return QMessageBox.question(parent, title, message, buttons)


###########Custom MessageBox#############
@dataclasses.dataclass
class MessageBoxConfig(object):
    """
    自定义消息框配置类。
    """

    text: str = ""
    """消息内容"""

    title: Optional[str] = None
    """对话框标题"""

    icon: Union[int, QPixmap, None] = None
    """对话框图标"""

    detailed_text: Optional[str] = None
    """详细消息内容"""

    informative_text: Optional[str] = None
    """提示性消息内容"""

    text_format: Optional[TextFormat] = None
    """消息内容格式"""

    buttons: Union[StandardButton, int, None] = None
    """对话框标准按钮"""

    default_button: Union[StandardButton, int, None] = None
    """默认按钮"""

    escape_button: Union[StandardButton, int, None] = None
    """取消按钮"""

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


def show_messagebox(parent: Optional[QWidget], **kwargs) -> Union[int, StandardButton]:
    """
    显示自定义消息框, 并返回用户点击的按钮的按键值。

    Args:
        parent: 父窗口
        **kwargs: 消息框配置参数，具体参数见MessageBoxConfig类。

    Returns:
        返回用户点击的按钮的按键值。
    """
    config = MessageBoxConfig(**kwargs)
    msg_box = config.create_messagebox(parent)
    ret_code = msg_box.exec_()
    msg_box.deleteLater()
    return ret_code


def show_exception_messagebox(
    parent: Optional[QWidget],
    exception: Exception,
    message: str = "",
    title: str = "Error",
    detail: bool = True,
    show_error_type: bool = True,
    **kwargs,
) -> Union[int, StandardButton]:
    """
    显示异常消息对话框。

    Args:
        parent: 父窗口
        exception: 异常对象
        message: 错误消息内容
        title: 对话框标题
        detail: 是否显示详细信息
        show_error_type: 是否显示异常类型
        **kwargs: 消息框其他配置参数，具体参数见MessageBoxConfig类。

    Returns:
        返回用户点击的按钮的按键值。
    """
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

    return show_messagebox(
        parent,
        text=error_msg,
        title=title,
        icon=QMessageBox.Critical,
        detailed_text=detail_msg,
        **kwargs,
    )


############Text Dialogs##############
class TextBrowserMessageBox(BaseCustomDialog):
    """
    文本浏览器消息框，用于展示长文本内容。
    """

    DEFAULT_SIZE = (585, 523)

    def __init__(
        self,
        parent: Optional[QWidget],
        text_content: str,
        text_format: Literal["markdown", "plaintext", "html"] = "markdown",
        size: Optional[Tuple[int, int]] = None,
        title: Optional[str] = None,
        icon: IconType = None,
        buttons: Optional[DialogButtons] = DialogButtonYes,
        resizeable: bool = True,
        **kwargs,
    ):
        """
        构造函数。

        Args:
            parent: 父窗口
            text_content: 文本内容
            text_format: 文本格式
            size: 对话框大小
            title: 对话框标题
            icon: 对话框图标
            buttons: 对话框按钮
            resizeable: 是否可调整大小
            **kwargs: 其他参数
        """
        super().__init__(parent, **kwargs)

        self._text_content = text_content
        self._text_format = text_format
        self._size = size or self.DEFAULT_SIZE
        self._title = title
        self._icon = icon
        self._buttons = buttons
        self._resizeable = resizeable

        # noinspection PyArgumentList
        self._button_box = QDialogButtonBox(self)
        # noinspection SpellCheckingInspection
        self._textbrowser = QTextBrowser(self)
        # noinspection PyArgumentList
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._setup_ui()

    def get_result(self) -> Any:
        return None

    # noinspection PyUnresolvedReferences
    def _setup_ui(self):
        if self._title is not None:
            self.setWindowTitle(self._title)

        if self._icon:
            icon = get_icon(self._icon) or QIcon()
            self.setWindowIcon(icon)

        if self._size:
            self.resize(*self._size)
            if not self._resizeable:
                self.setFixedSize(*self._size)

        if self._buttons is not None:
            self._button_box.setStandardButtons(self._buttons)
            self._button_box.accepted.connect(self.accept)
            self._button_box.rejected.connect(self.reject)
        else:
            self._button_box.hide()

        if self._text_content:
            self._textbrowser.setOpenLinks(True)
            self._textbrowser.setOpenExternalLinks(True)
            if self._text_format == "markdown":
                self._textbrowser.setMarkdown(self._text_content)
            elif self._text_format == "html":
                self._textbrowser.setHtml(self._text_content)
            elif self._text_format == "plaintext":
                self._textbrowser.setPlainText(self._text_content)
            else:
                self._textbrowser.setText(self._text_content)

        self._layout.addWidget(self._textbrowser)
        self._layout.addWidget(self._button_box)


def show_text_content(
    parent: Optional[QWidget],
    text_content: str,
    text_format: Literal["markdown", "plaintext", "html"] = "markdown",
    size: Optional[Tuple[int, int]] = None,
    title: Optional[str] = None,
    icon: IconType = None,
    buttons: Optional[DialogButtons] = DialogButtonOk,
    resizeable: bool = True,
) -> None:
    """
    显示文本内容对话框。

    Args:
        parent: 父窗口
        text_content: 文本内容
        text_format: 文本格式
        size: 对话框大小
        title: 对话框标题
        icon: 对话框图标
        buttons: 对话框按钮
        resizeable: 是否可调整大小

    Returns:
        无返回值
    """
    TextBrowserMessageBox.show_and_get_result(
        parent,
        text_content=text_content,
        text_format=text_format,
        size=size,
        title=title,
        icon=icon,
        buttons=buttons,
        resizeable=resizeable,
    )


def show_text_file(
    parent: Optional[QWidget],
    text_file: str,
    text_format: Literal["markdown", "plaintext", "html"] = "markdown",
    size: Tuple[int, int] = None,
    title: Optional[str] = "",
    icon: IconType = None,
    buttons: Optional[DialogButtons] = DialogButtonOk,
    resizeable: bool = True,
) -> None:
    """
    显示文本文件内容对话框。

    Args:
        parent: 父窗口
        text_file: 文本文件路径
        text_format: 文本格式
        size: 对话框大小
        title: 对话框标题
        icon: 对话框图标
        buttons: 对话框按钮
        resizeable: 是否可调整大小

    Returns:
        无返回值
    """
    text_content = read_text_file(text_file)
    show_text_content(
        parent,
        text_content=text_content,
        text_format=text_format,
        size=size,
        title=title,
        icon=icon,
        buttons=buttons,
        resizeable=resizeable,
    )
