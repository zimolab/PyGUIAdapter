"""
@Time    : 2024.10.20
@File    : ubeep.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 提供了发出蜂鸣声的功能
"""

from qtpy.QtWidgets import QApplication


def beep() -> None:
    """
    发出蜂鸣声。

    Returns:
        无返回值
    """
    QApplication.beep()
