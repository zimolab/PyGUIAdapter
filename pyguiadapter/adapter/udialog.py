from concurrent.futures import Future
from typing import Any, Literal, Tuple, Type, Optional, Union

from qtpy.QtGui import QPixmap

from .ucontext import _context
from ..utils import IconType, InformationIcon, WarningIcon, CriticalIcon, QuestionIcon
from ..utils import io
from ..utils.dialog import BaseCustomDialog
from ..utils.messagebox import (
    TextBrowserMessageBox,
    StandardButton,
    Ok,
    Yes,
    No,
    NoButton,
    DialogButtons,
    DialogButtonOk,
    MessageBoxIcon,
)


def show_custom_dialog(dialog_class: Type[BaseCustomDialog], **kwargs) -> Any:
    """
    弹出自定义对话框。

    Args:
        dialog_class: 自定义对话框类
        **kwargs: 自定义对话框初始化参数

    Returns:
        返回自定义对话框`show_and_get_result()`函数的返回值。
    """
    result_future = Future()
    # noinspection PyUnresolvedReferences
    _context.sig_show_custom_dialog.emit(result_future, dialog_class, kwargs)
    return result_future.result()


def _show_messagebox(
    text: str,
    icon: Union[MessageBoxIcon, int, QPixmap],
    title: str = "Information",
    buttons: Union[StandardButton, int] = Ok,
    default_button: Union[StandardButton, int] = NoButton,
    **kwargs,
) -> Union[int, StandardButton]:
    result_future = Future()
    # noinspection PyUnresolvedReferences
    args = dict(
        text=text,
        title=title,
        icon=icon,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )
    _context.sig_show_messagebox.emit(result_future, args)
    return result_future.result()


def show_info_messagebox(
    text: str,
    title: str = "Information",
    buttons: Union[StandardButton, int] = Ok,
    default_button: Union[StandardButton, int] = Ok,
    **kwargs,
) -> Union[int, StandardButton]:
    """
    弹出Information消息对话框。

    Args:
        text: 消息文本
        title:  对话框标题
        buttons:  对话框的按钮
        default_button: 默认按钮
        **kwargs: 其他参数

    Returns:
        返回用户按下的按钮。
    """
    return _show_messagebox(
        text=text,
        icon=InformationIcon,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_warning_messagebox(
    text: str,
    title: str = "Warning",
    buttons: Union[StandardButton, int] = Ok,
    default_button: Union[StandardButton, int] = Ok,
    **kwargs,
) -> Union[int, StandardButton]:
    """
    弹出Warning消息对话框。

    Args:
        text: 消息文本
        title:  对话框标题
        buttons:  对话框的按钮
        default_button: 默认按钮
        **kwargs: 其他参数

    Returns:
        返回用户按下的按钮。
    """
    return _show_messagebox(
        text=text,
        icon=WarningIcon,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_critical_messagebox(
    text: str,
    title: str = "Critical",
    buttons: Union[StandardButton, int] = Ok,
    default_button: Union[StandardButton, int] = NoButton,
    **kwargs,
) -> Union[int, StandardButton]:
    """
    弹出Critical消息对话框。

    Args:
        text: 消息文本
        title:  对话框标题
        buttons:  对话框的按钮
        default_button: 默认按钮
        **kwargs: 其他参数

    Returns:
        返回用户按下的按钮。
    """
    return _show_messagebox(
        text=text,
        icon=CriticalIcon,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_question_messagebox(
    text: str,
    title: str = "Question",
    buttons: Union[StandardButton, int] = Yes | No,
    default_button: Union[StandardButton, int] = NoButton,
    **kwargs,
) -> Union[int, StandardButton]:
    """
    弹出Question消息对话框。

    Args:
        text: 消息文本
        title:  对话框标题
        buttons:  对话框的按钮
        default_button: 默认按钮
        **kwargs: 其他参数

    Returns:
        返回用户按下的按钮。
    """
    return _show_messagebox(
        text=text,
        icon=QuestionIcon,
        title=title,
        buttons=buttons,
        default_button=default_button,
        **kwargs,
    )


def show_text_content(
    text_content: str,
    text_format: Literal["markdown", "plaintext", "html"] = "markdown",
    size: Tuple[int, int] = None,
    title: Optional[str] = "",
    icon: IconType = None,
    buttons: Optional[DialogButtons] = DialogButtonOk,
    resizeable: bool = True,
) -> None:
    """
    显示多行文本内容。

    Args:
        text_content: 文本内容
        text_format: 文本格式
        size: 对话框尺寸
        title: 对话框标题
        icon: 对话框图标
        buttons: 对话框按钮
        resizeable: 对话框是否可调整大小

    Returns:
        无返回值
    """
    return show_custom_dialog(
        TextBrowserMessageBox,
        text_content=text_content,
        text_format=text_format,
        size=size,
        title=title,
        icon=icon,
        buttons=buttons,
        resizeable=resizeable,
    )


def show_text_file(
    text_file: str,
    text_format: Literal["markdown", "plaintext", "html"] = "markdown",
    size: Tuple[int, int] = None,
    title: Optional[str] = "",
    icon: IconType = None,
    buttons: Optional[DialogButtons] = DialogButtonOk,
    resizeable: bool = True,
) -> None:
    """
    展示文本文件内容。

    Args:
        text_file: 文本文件路径
        text_format: 文本文件格式
        size: 对话框尺寸
        title: 对话框标题
        icon: 对话框图标
        buttons: 对话框按钮
        resizeable: 对话框是否可调整大小

    Returns:
        无返回值
    """
    text_content = io.read_text_file(text_file)
    return show_text_content(
        text_content=text_content,
        text_format=text_format,
        size=size,
        title=title,
        icon=icon,
        buttons=buttons,
        resizeable=resizeable,
    )
