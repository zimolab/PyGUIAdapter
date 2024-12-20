"""
@Time    : 2024.10.20
@File    : uprogress.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 提供进度条相关的功能
"""

from typing import Literal, Optional

from .ucontext import _context


def show_progressbar(
    min_value: int = 0,
    max_value: int = 100,
    inverted_appearance: bool = False,
    *,
    message_visible: bool = False,
    message_format: str = "%p%",
    message_centered: str = True,
    info_visible: bool = True,
    info_centered: bool = True,
    info_text_format: Literal[
        "richtext", "markdown", "plaintext", "autotext"
    ] = "autotext",
    initial_info: str = "",
) -> None:
    """
    显示进度条。默认情况下，进度条处于隐藏状态，开发者必须手动调用此函数来显示进度条，此函数除了用于显示进度条，还可以对进度条进行配置。

    Args:
        min_value: 最小进度值，默认为`0`
        max_value: 最大进度值，默认为`100`
        inverted_appearance: 是否改变进度条的显示方式，使其以反方向显示进度
        message_visible: 是否显示message信息
        message_format: message信息的格式，支持：`%p%`（显示完成的百分比，这是默认显示方式）、`%v`（显示当前的进度值）和`%m`（显示总的步进值）
        message_centered: message信息是否居中显示
        info_visible: 是否显示info区域
        info_centered: info信息是否居中显示
        info_text_format: info信息的文本格式，支持`"richtext"` 、` "markdown"` 、`"plaintext"` 、`"autotext"`
        initial_info: info信息的初始值

    Returns:
        无返回值
    """
    config = {
        "min_value": min_value,
        "max_value": max_value,
        "inverted_appearance": inverted_appearance,
        "message_visible": message_visible,
        "message_format": message_format,
        "message_centered": message_centered,
        "show_info_label": info_visible,
        "info_text_centered": info_centered,
        "info_text_format": info_text_format,
        "initial_info": initial_info,
    }
    _context.sig_show_progressbar.emit(config)


def hide_progressbar() -> None:
    """
    隐藏进度条

    Returns:
        无返回值
    """
    _context.sig_hide_progressbar.emit()


def update_progress(value: int, info: Optional[str] = None) -> None:
    """
    更新进度信息

    Args:
        value: 当前进度值
        info:  当前info文本

    Returns:
        无返回值
    """
    _context.sig_update_progressbar.emit(value, info)


def show_progress_dialog(
    min_value: int = 0,
    max_value: int = 100,
    inverted_appearance: bool = False,
    *,
    message_visible: bool = False,
    message_format: str = "%p%",
    message_centered: str = True,
    info_visible: bool = True,
    info_centered: bool = True,
    info_text_format: Literal[
        "richtext", "markdown", "plaintext", "autotext"
    ] = "autotext",
    initial_info: str = "",
    title: str = "Progress",
    size: tuple = (400, 150),
    modal: bool = True,
) -> None:
    """
    显示进度对话框。开发者必须手动调用此函数来显示进度对话框，此函数除了用于显示进度对话框，
    还用于对进度对话框进行配置。

    Args:
        min_value: 最小进度值，默认为`0`
        max_value: 最大进度值，默认为`100`
        inverted_appearance: 是否改变进度条的显示方式，使其以反方向显示进度
        message_visible: 是否显示message信息
        message_format: message信息的格式，支持：`%p%`（显示完成的百分比，这是默认显示方式）、`%v`（显示当前的进度值）和`%m`（显示总的步进值）
        message_centered: message信息是否居中显示
        info_visible: 是否显示info信息
        info_centered: info信息是否居中显示
        info_text_format: info信息的文本格式，支持`"richtext"` 、` "markdown"` 、`"plaintext"` 、`"autotext"`
        initial_info: info信息的初始值
        title: 对话框标题
        size: 对话框大小
        modal: 是否为模态对话框
    Returns:
        无返回值
    """
    _context.sig_show_progress_dialog.emit(
        {
            "min_value": min_value,
            "max_value": max_value,
            "inverted_appearance": inverted_appearance,
            "title": title,
            "message_visible": message_visible,
            "message_format": message_format,
            "message_centered": message_centered,
            "info_visible": info_visible,
            "info_centered": info_centered,
            "info_text_format": info_text_format,
            "initial_info": initial_info,
            "size": size,
            "modal": modal,
        }
    )


def dismiss_progress_dialog() -> None:
    """
    关闭进度对话框

    Returns:
        无返回值
    """
    _context.sig_dismiss_progress_dialog.emit()


def update_progress_dialog(value: int, info: Optional[str] = None) -> None:
    """
    更新进度对话框

    Args:
        value: 当前进度值
        info:  当前info文本
    Returns:
        无返回值
    """
    _context.sig_update_progress_dialog.emit(value, info)
