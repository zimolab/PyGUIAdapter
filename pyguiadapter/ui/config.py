import dataclasses
import warnings
from typing import Optional, Union

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QDialog

from pyguiadapter.commons import safe_read


@dataclasses.dataclass
class WindowConfig(object):
    title: Optional[str] = None
    icon: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    x: Optional[int] = None
    y: Optional[int] = None

    stylesheet: Optional[str] = None

    def apply_to(self, w: Union[QMainWindow, QDialog]) -> None:
        if self.title is not None:
            w.setWindowTitle(self.title)
        if self.icon is not None:
            self._set_icon(w)
        if self.width is not None and self.height is not None:
            w.resize(self.width, self.height)
        if self.x is not None and self.y is not None:
            w.move(self.x, self.y)

        if self.stylesheet:
            stylesheet = safe_read(self.stylesheet)
            if stylesheet is not None:
                w.setStyleSheet(stylesheet)
            else:
                w.setStyleSheet(self.stylesheet)

    def _set_icon(self, w: Union[QMainWindow, QDialog]):
        if self.icon is None:
            return
        try:
            icon = QIcon(self.icon)
        except BaseException as e:
            warnings.warn(w.tr(f"failed to load icon {self.icon}: {e}"))
        else:
            w.setWindowIcon(icon)
