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
from ..editor_base import DialogBasedItemsViewEditor
from ..itemsview_base import ItemsViewFrameBase

DEFAULT_WINDOW_SIZE = (800, 600)


@dataclasses.dataclass
class PathListEditorConfig(PathListViewFrameConfig):
    # assign None to hide the add_button by default
    add_button_text: Optional[str] = None
    window_title: str = ""
    window_size: Tuple[int, int] = DEFAULT_WINDOW_SIZE


class PathListEditor(DialogBasedItemsViewEditor):
    def __init__(
        self,
        parent: Optional[QWidget],
        config: PathListEditorConfig,
    ):
        self._config = config
        self._listview_frame: Optional[PathListViewFrame] = None

        super().__init__(parent)

        if self._config.window_title:
            self.setWindowTitle(self._config.window_title)
        if self._config.window_size:
            self.resize(*self._config.window_size)

    def set_path_list(self, path_list: List[str]):
        self._list_frame.items_view.remove_all_rows()
        for path in path_list:
            self._list_frame.items_view.append_row(path)

    def get_path_list(self) -> List[str]:
        return self._list_frame.items_view.get_all_row_data()

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

    def create_items_view_frame(self) -> ItemsViewFrameBase:
        if self._listview_frame is None:
            self._listview_frame = PathListViewFrame(self, self._config)
        return self._listview_frame
