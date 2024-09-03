from __future__ import annotations

import dataclasses
import os.path
from typing import Type, TypeVar, List, Literal

from qtpy.QtCore import QStringListModel, Qt
from qtpy.QtWidgets import QWidget, QListView, QGridLayout, QVBoxLayout, QPushButton

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils

TextElideMode = Qt.TextElideMode


@dataclasses.dataclass(frozen=True)
class StringListEditConfig(CommonParameterWidgetConfig):
    default_value: List[str] | None = None
    empty_string_strategy: Literal["keep_all", "keep_one", "remove_all"] = "remove_all"
    select_file: bool = True
    select_directory: bool = True
    file_filters: str = ""
    start_dir: str = ""
    normalize_path: bool = True
    add_button_text: str = "Add"
    remove_button_text: str = "Remove"
    select_file_button_text: str = "File"
    select_directory_button_text: str = "Directory"
    file_dialog_title: str = "Select File"
    directory_dialog_title: str = "Select Directory"
    min_height: int = 300
    drag_enabled: bool = True
    wrapping: bool = False
    text_elide_mode: TextElideMode = TextElideMode.ElideLeft
    alternating_row_colors: bool = True
    confirm_remove: bool = True

    @classmethod
    def target_widget_class(cls) -> Type["StringListEdit"]:
        return StringListEdit


class StringListEdit(CommonParameterWidget):
    Self = TypeVar("Self", bound="StringListEdit")
    ConfigClass = StringListEditConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: StringListEditConfig,
    ):
        self._config: StringListEditConfig = config
        self._value_widget: QWidget | None = None
        self._list_view: QListView | None = None
        self._add_button: QPushButton | None = None
        self._remove_button: QPushButton | None = None
        self._select_file_button: QPushButton | None = None
        self._select_directory_button: QPushButton | None = None

        self._model: QStringListModel | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            layout_main = QVBoxLayout(self._value_widget)
            layout_main.setContentsMargins(0, 0, 0, 0)
            layout_main.setSpacing(0)
            self._value_widget.setLayout(layout_main)

            self._list_view = QListView(self._value_widget)
            if self._config.min_height > 0:
                self._list_view.setMinimumHeight(self._config.min_height)
            if self._config.drag_enabled:
                self._list_view.setDragDropMode(QListView.InternalMove)
                self._list_view.setDefaultDropAction(Qt.DropAction.TargetMoveAction)
                self._list_view.setMovement(QListView.Snap)
                self._list_view.setDragDropOverwriteMode(False)
            self._list_view.setWrapping(self._config.wrapping)
            self._list_view.setTextElideMode(self._config.text_elide_mode)
            self._list_view.setAlternatingRowColors(self._config.alternating_row_colors)

            self._model = QStringListModel(self._value_widget)
            self._list_view.setModel(self._model)
            layout_main.addWidget(self._list_view)

            layout_buttons = QGridLayout(self._value_widget)

            self._add_button = QPushButton(
                self._config.add_button_text, self._value_widget
            )
            # noinspection PyUnresolvedReferences
            self._add_button.clicked.connect(self._on_add_item)
            layout_buttons.addWidget(self._add_button, 1, 0)

            self._remove_button = QPushButton(
                self._config.remove_button_text, self._value_widget
            )
            # noinspection PyUnresolvedReferences
            self._remove_button.clicked.connect(self._on_remove_item)
            layout_buttons.addWidget(self._remove_button, 1, 1)

            if self._config.select_file:
                self._select_file_button = QPushButton(
                    self._config.select_file_button_text, self._value_widget
                )
                # noinspection PyUnresolvedReferences
                self._select_file_button.clicked.connect(self._on_select_file)
                layout_buttons.addWidget(self._select_file_button, 2, 0)

            if self._config.select_directory:
                self._select_directory_button = QPushButton(
                    self._config.select_directory_button_text, self._value_widget
                )
                # noinspection PyUnresolvedReferences
                self._select_directory_button.clicked.connect(self._on_select_directory)
                layout_buttons.addWidget(self._select_directory_button, 2, 1)
            layout_main.addLayout(layout_buttons)
        return self._value_widget

    def set_value_to_widget(self, value: List[str]):
        self._clear_items()
        self._append_items(value)

    def get_value_from_widget(self) -> List[str]:
        string_list = self._model.stringList()
        if self._config.empty_string_strategy == "keep_all":
            return string_list.copy()
        elif self._config.empty_string_strategy == "keep_one":
            return self._keep_one_empty_item(string_list)
        else:
            return [item for item in string_list if item != ""]

    def _on_add_item(self):
        self._append_item("", edit=True, set_current=True)

    def _on_remove_item(self):
        selected = self._list_view.selectedIndexes()
        if not selected:
            utils.show_warning_message(self, "No item selected!", title="Warning")
            return
        if self._config.confirm_remove:
            ret = utils.show_question_message(
                self,
                message=f"{len(selected)} item(s) are selected. Are you sure to remove them?",
                title="Confirm",
                buttons=utils.StandardButton.Yes | utils.StandardButton.No,
            )
            if ret == utils.StandardButton.No:
                return
        for index in selected:
            self._model.removeRow(index.row())

    def _on_select_file(self):
        current_idx = self._list_view.currentIndex()
        path = utils.get_open_file(
            self,
            title=self._config.file_dialog_title,
            start_dir=self._config.start_dir,
            filters=self._config.file_filters,
        )
        if not path:
            return
        if self._config.normalize_path:
            path = os.path.normpath(path)
        if not current_idx or not current_idx.isValid():
            self._append_item(path, set_current=True)
        else:
            self._model.setData(current_idx, path)

    def _on_select_directory(self):
        current_idx = self._list_view.currentIndex()
        path = utils.get_existing_directory(
            self,
            title=self._config.file_dialog_title,
            start_dir=self._config.start_dir,
        )
        if not path:
            return
        if self._config.normalize_path:
            path = os.path.normpath(path)
        if not current_idx or not current_idx.isValid():
            self._append_item(path, set_current=True)
        else:
            self._model.setData(current_idx, path)

    def _clear_items(self):
        self._model.removeRows(0, self._model.rowCount())

    def _append_item(self, item: str, edit: bool = False, set_current: bool = False):
        self._model.insertRow(self._model.rowCount())
        self._model.setData(self._model.index(self._model.rowCount() - 1), item)
        if edit:
            self._list_view.edit(self._model.index(self._model.rowCount() - 1))
        if set_current:
            self._list_view.setCurrentIndex(
                self._model.index(self._model.rowCount() - 1)
            )

    def _append_items(self, items: List[str]):
        for item in items:
            self._append_item(item, set_current=False)

    @staticmethod
    def _keep_one_empty_item(items: List[str]) -> List[str]:
        should_add = True
        ret = []
        for item in items:
            if item != "":
                ret.append(item)
                continue
            # if item == "" and
            if should_add:
                ret.append(item)
                should_add = False
        return ret
