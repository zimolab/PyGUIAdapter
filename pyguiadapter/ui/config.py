import dataclasses
import warnings

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QDialog

from pyguiadapter.commons import safe_read


@dataclasses.dataclass
class WindowConfig(object):
    title: str | None = None
    icon: str | None = None
    width: int | None = None
    height: int | None = None
    x: int | None = None
    y: int | None = None

    stylesheet: str | None = None

    def apply_to(self, w: QMainWindow | QDialog) -> None:
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

    def _set_icon(self, w: QMainWindow | QDialog):
        if self.icon is None:
            return
        try:
            icon = QIcon(self.icon)
        except BaseException as e:
            warnings.warn(w.tr(f"failed to load icon {self.icon}: {e}"))
        else:
            w.setWindowIcon(icon)
