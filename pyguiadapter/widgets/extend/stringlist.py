import dataclasses
import os.path
from typing import Type, List, Literal, Optional

from qtpy.QtCore import QStringListModel, Qt
from qtpy.QtWidgets import QWidget, QListView, QVBoxLayout, QPushButton, QMenu, QAction

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils

TextElideMode = Qt.TextElideMode


@dataclasses.dataclass(frozen=True)
class StringListEditConfig(CommonParameterWidgetConfig):
    default_value: Optional[List[str]] = dataclasses.field(default_factory=list)
    empty_string_strategy: Literal["keep_all", "keep_one", "remove_all"] = "remove_all"
    add_file: bool = True
    add_dir: bool = True
    file_filters: str = ""
    start_dir: str = ""
    normalize_path: bool = True
    add_button_text: str = "Add"
    remove_button_text: str = "Remove"
    clear_button_text: str = "Clear"
    add_string_hint: str = "Add Text"
    add_file_hint: str = "Add File"
    add_dir_hint: str = "Add Directory"
    file_dialog_title: str = "Select File"
    dir_dialog_title: str = "Select Directory"
    confirm_dialog_title: str = "Confirm"
    warning_dialog_title: str = "Warning"
    remove_confirm_message: str = "Are you sure to remove the selected item(s)?"
    clear_confirm_message: str = "Are you sure to clear all of the items?"
    no_selection_message: str = "No items are selected!"
    min_height: int = 230
    drag_enabled: bool = True
    wrapping: bool = False
    text_elide_mode: TextElideMode = TextElideMode.ElideLeft
    alternating_row_colors: bool = True
    confirm_remove: bool = True

    @classmethod
    def target_widget_class(cls) -> Type["StringListEdit"]:
        return StringListEdit


class StringListEdit(CommonParameterWidget):
    ConfigClass = StringListEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: StringListEditConfig,
    ):
        self._value_widget: Optional[QWidget] = None
        self._list_view: Optional[QListView] = None
        self._add_button: Optional[QPushButton] = None
        self._remove_button: Optional[QPushButton] = None
        self._clear_button: Optional[QPushButton] = None

        self._model: Optional[QStringListModel] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: StringListEditConfig
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            layout_main = QVBoxLayout()
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

            layout_buttons = QVBoxLayout(self._value_widget)

            self._add_button = self._create_add_button(self._value_widget)
            layout_buttons.addWidget(self._add_button)

            self._remove_button = QPushButton(self._value_widget)
            self._remove_button.setText(self._config.remove_button_text)
            # noinspection PyUnresolvedReferences
            self._remove_button.clicked.connect(self._on_remove_item)
            layout_buttons.addWidget(self._remove_button)

            self._clear_button = QPushButton(self._value_widget)
            # noinspection PyUnresolvedReferences
            self._clear_button.clicked.connect(self._on_clear_items)
            self._clear_button.setText(self._config.clear_button_text)
            layout_buttons.addWidget(self._clear_button)

            layout_main.addLayout(layout_buttons)
        return self._value_widget

    def _create_add_button(self, parent: QWidget) -> QPushButton:
        self._config: StringListEditConfig
        add_button = QPushButton(parent)
        add_button.setText(self._config.add_button_text)
        if self._config.add_file or self._config.add_dir:
            menu = QMenu(add_button)

            action_add_string = QAction(menu)
            action_add_string.setText(self._config.add_string_hint)
            # noinspection PyUnresolvedReferences
            action_add_string.triggered.connect(self._on_add_item)
            menu.addAction(action_add_string)

            if self._config.add_file:
                action_add_file = QAction(menu)
                action_add_file.setText(self._config.add_file_hint)
                # noinspection PyUnresolvedReferences
                action_add_file.triggered.connect(self._on_add_file)
                menu.addAction(action_add_file)
            if self._config.add_dir:
                action_add_dir = QAction(menu)
                action_add_dir.setText(self._config.add_dir_hint)
                # noinspection PyUnresolvedReferences
                action_add_dir.triggered.connect(self._on_add_dir)
                menu.addAction(action_add_dir)
            add_button.setMenu(menu)
        else:
            # noinspection PyUnresolvedReferences
            add_button.clicked.connect(self._on_add_item)
        return add_button

    def set_value_to_widget(self, value: List[str]):
        self._clear_items()
        self._append_items(value)

    def get_value_from_widget(self) -> List[str]:
        self._config: StringListEditConfig
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
        self._config: StringListEditConfig
        selected = self._list_view.selectedIndexes()
        if not selected:
            utils.show_warning_message(
                self,
                self._config.no_selection_message,
                title=self._config.warning_dialog_title,
            )
            return
        if self._config.confirm_remove:
            ret = utils.show_question_message(
                self,
                message=self._config.remove_confirm_message,
                title=self._config.warning_dialog_title,
                buttons=utils.StandardButton.Yes | utils.StandardButton.No,
            )
            if ret == utils.StandardButton.No:
                return
        for index in selected:
            self._model.removeRow(index.row())

    def _on_clear_items(self):
        self._config: StringListEditConfig
        count = self._model.rowCount()
        if count <= 0:
            return
        if self._config.confirm_remove:
            ret = utils.show_question_message(
                self,
                message=self._config.clear_confirm_message,
                title=self._config.warning_dialog_title,
                buttons=utils.StandardButton.Yes | utils.StandardButton.No,
            )
            if ret == utils.StandardButton.No:
                return
        self._clear_items()

    def _on_add_file(self):
        self._config: StringListEditConfig
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
        current_idx = self._list_view.currentIndex()
        if not current_idx or (not current_idx.isValid()):
            self._append_item(path, set_current=False)
        else:
            self._model.setData(current_idx, path)

    def _on_add_dir(self):
        self._config: StringListEditConfig
        path = utils.get_existing_directory(
            self,
            title=self._config.file_dialog_title,
            start_dir=self._config.start_dir,
        )
        if not path:
            return
        if self._config.normalize_path:
            path = os.path.normpath(path)
        current_idx = self._list_view.currentIndex()
        if not current_idx or (not current_idx.isValid()):
            self._append_item(path, set_current=True)
        else:
            self._model.setData(current_idx, path)

    def _clear_items(self):
        self._model.removeRows(0, self._model.rowCount())
        self._model.setStringList([])

    def _append_item(self, item: str, edit: bool = False, set_current: bool = False):
        row = self._model.rowCount()
        self._model.insertRow(row)
        self._model.setData(self._model.index(row), item)
        if edit:
            self._list_view.edit(self._model.index(row))
        if set_current:
            self._list_view.setCurrentIndex(self._model.index(row))

    def _append_items(self, items: List[str]):
        for item in items:
            self._append_item(item)

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
