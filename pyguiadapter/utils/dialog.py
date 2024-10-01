from abc import abstractmethod
from typing import Optional, Any, Tuple

from qtpy.QtWidgets import QDialog, QWidget


class BaseCustomDialog(QDialog):
    def __init__(self, parent: Optional[QWidget], **kwargs):
        super().__init__(parent)

    @abstractmethod
    def get_result(self) -> Any:
        pass

    @classmethod
    def new_instance(cls, parent: QWidget, **kwargs) -> "BaseCustomDialog":
        return cls(parent, **kwargs)

    @classmethod
    def show_and_get_result(
        cls, parent: Optional[QWidget], **kwargs
    ) -> Tuple[int, Any]:
        dialog = cls.new_instance(parent, **kwargs)
        ret_code = dialog.exec_()
        result = None
        if ret_code == QDialog.Accepted:
            result = dialog.get_result()
        dialog.deleteLater()
        return result
