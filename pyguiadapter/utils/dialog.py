"""
@Time    : 2024.10.20
@File    : dialog.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 定义了自定义对话框基类。
"""

from abc import abstractmethod
from typing import Optional, Any

from qtpy.QtWidgets import QDialog, QWidget


class BaseCustomDialog(QDialog):
    """
    自定义对话框基类，可用于实现自定义消息对话框、自定义输入对话框等。
    """

    def __init__(self, parent: Optional[QWidget], **kwargs):
        super().__init__(parent)

    @abstractmethod
    def get_result(self) -> Any:
        """
        获取对话框的结果。

        Returns:
            对话框的结果。
        """
        pass

    @classmethod
    def new_instance(cls, parent: QWidget, **kwargs) -> "BaseCustomDialog":
        return cls(parent, **kwargs)

    @classmethod
    def show_and_get_result(cls, parent: Optional[QWidget], **kwargs) -> Any:
        """
        显示对话框并获取结果。

        Args:
            parent: 父窗口
            **kwargs: 构造函数参数

        Returns:
            结果元组，第一个元素为返回码，第二个元素为对话框的结果。
        """
        dialog = cls.new_instance(parent, **kwargs)
        ret_code = dialog.exec_()
        result = None
        if ret_code == QDialog.Accepted:
            result = dialog.get_result()
        dialog.deleteLater()
        return result
