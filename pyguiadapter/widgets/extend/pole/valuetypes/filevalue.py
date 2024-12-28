from pathlib import Path
from typing import Optional

from qtpy.QtCore import QModelIndex
from qtpy.QtWidgets import (
    QFileDialog,
    QWidget,
    QStyleOptionViewItem,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

from .base import ValueWidgetMixin, ValueTypeBase

DEFAULT_VALUE = ""


class FilePathEditor(QFileDialog, ValueWidgetMixin):

    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        *,
        title: Optional[str] = None,
        filters: Optional[str] = None,
        start_dir: Optional[str] = None,
        as_posix: bool = True
    ):
        super().__init__(parent)

        self.as_posix = as_posix

        if title:
            self.setWindowTitle(title)

        if filters:
            self.setNameFilter(filters)

        if start_dir:
            self.setDirectory(start_dir)

        self.setFileMode(QFileDialog.ExistingFile)
        self.setAcceptMode(QFileDialog.AcceptOpen)

        self._init_value = default_value
        self.setModal(True)

    def get_value(self) -> str:
        selected_files = self.selectedFiles()
        if selected_files:
            selected_file = selected_files[0]
            if self.as_posix:
                selected_file = Path(selected_file).absolute().as_posix()
            return selected_file
        else:
            return self._init_value

    def set_value(self, value: str):
        self._init_value = value


class FilePathEdit(QWidget, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: str,
        *,
        browse_button_text: str = "Browse",
        title: Optional[str] = None,
        filters: Optional[str] = None,
        start_dir: Optional[str] = None,
        as_posix: bool = True
    ):
        super().__init__(parent)
        self.title = title
        self.filters = filters
        self.start_dir = start_dir
        self.as_posix = as_posix

        self._init_value = default_value

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._edit = QLineEdit(self)
        self._edit.setText(default_value)
        self._layout.addWidget(self._edit)

        self._button = QPushButton(self)
        # noinspection PyUnresolvedReferences
        self._button.clicked.connect(self._on_browse_file)
        self._button.setText(browse_button_text)
        self._layout.addWidget(self._button)

    def _on_browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, self.title, self.start_dir, self.filters
        )
        if not filename:
            return
        if self.as_posix:
            filename = Path(filename).absolute().as_posix()
        self._edit.setText(filename)

    def get_value(self) -> str:
        return self._edit.text()

    def set_value(self, value: str):
        self._edit.setText(value)


class FilePathValue(ValueTypeBase):
    def __init__(
        self,
        default_value: str = DEFAULT_VALUE,
        *,
        title: Optional[str] = None,
        filters: Optional[str] = None,
        start_dir: Optional[str] = None,
        as_posix: bool = True
    ):
        super().__init__(default_value)
        self.title = title
        self.filters = filters
        self.start_dir = start_dir
        self.as_posix = as_posix

    def on_create_editor(
        self,
        parent: QWidget,
        option: Optional[QStyleOptionViewItem],
        index: Optional[QModelIndex],
        **kwargs
    ) -> QWidget:
        _ = option, index, kwargs  # unused
        editor = FilePathEditor(
            parent,
            default_value=self.default_value,
            title=self.title,
            filters=self.filters,
            start_dir=self.start_dir,
            as_posix=self.as_posix,
        )
        return editor

    def on_create_edit(self, parent: QWidget, **kwargs) -> QWidget:
        edit = FilePathEdit(
            parent,
            default_value=self.default_value,
            title=self.title,
            filters=self.filters,
            start_dir=self.start_dir,
            as_posix=self.as_posix,
        )
        return edit
