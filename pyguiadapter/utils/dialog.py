from abc import abstractmethod
from typing import Optional, Any

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
