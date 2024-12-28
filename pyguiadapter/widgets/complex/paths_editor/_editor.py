import dataclasses
from typing import Optional, List, Tuple

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
    QMessageBox,
    QGroupBox,
)

from ._frame import PathListViewFrame, PathListViewFrameConfig

DEFAULT_WINDOW_SIZE = (800, 600)


@dataclasses.dataclass
class PathListEditorConfig(PathListViewFrameConfig):
    # assign None to hide the add_button by default
    add_button_text: Optional[str] = None
    window_title: str = ""
    window_size: Tuple[int, int] = DEFAULT_WINDOW_SIZE


class PathListEditor(QDialog):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        config: Optional[PathListEditorConfig] = None,
    ):
        self._config = config or PathListEditorConfig()
        super().__init__(parent)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._container = QGroupBox(self)
        self._container.setTitle(self._config.path_list_label_text)
        self._layout.addWidget(self._container)

        self._container_layout = QVBoxLayout()
        self._container_layout.setContentsMargins(0, 0, 0, 0)
        self._container.setLayout(self._container_layout)

        self._list_frame = PathListViewFrame(self._container, self._config)
        self._container_layout.addWidget(self._list_frame)

        self._dialog_button_box = QDialogButtonBox(self)
        self._dialog_button_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        # noinspection PyUnresolvedReferences
        self._dialog_button_box.accepted.connect(self.on_accept)
        # noinspection PyUnresolvedReferences
        self._dialog_button_box.rejected.connect(self.on_reject)
        self._layout.addWidget(self._dialog_button_box)

        if self._config.window_title:
            self.setWindowTitle(self._config.window_title)
        if self._config.window_size:
            self.resize(*self._config.window_size)
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

    def set_path_list(self, path_list: List[str]):
        self._list_frame.items_view.remove_all_rows()
        for path in path_list:
            self._list_frame.items_view.append_row(path)

    def get_path_list(self) -> List[str]:
        return self._list_frame.items_view.get_all_row_data()

    def on_accept(self):
        self.accept()

    def on_reject(self):
        self.reject()

    def closeEvent(self, event):
        if self._config.exit_confirm_message:
            ret = QMessageBox.question(
                self,
                "Exit Confirmation",
                self._config.exit_confirm_message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if ret == QMessageBox.No:
                event.ignore()
                return
        super().closeEvent(event)

    def start(self, path_list: Optional[List[str]] = None) -> List[str]:
        if path_list is None:
            path_list = []
        self.set_path_list(path_list)
        ret = self.exec_()
        if ret == QDialog.Accepted:
            return self.get_path_list()
        else:
            return path_list
