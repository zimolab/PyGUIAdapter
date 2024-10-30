import dataclasses
import os.path
from typing import Type, List, Literal, Optional, Any, Callable

from qtpy.QtCore import QStringListModel, Qt, QMimeData, QUrl, QModelIndex
from qtpy.QtWidgets import (
    QWidget,
    QListView,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
    QDialog,
    QLineEdit,
    QSpacerItem,
    QSizePolicy,
)

from ._dnd import default_dnd_filter
from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils
from ...utils import type_check

TextElideMode = Qt.TextElideMode
"""文本省略模式"""


@dataclasses.dataclass(frozen=True)
class PathEditDialogConfig(object):
    """PathEditDialog的配置类。"""

    title: str = "Edit Path"
    """对话框标题"""

    select_file: bool = True
    """是否开启选择文件功能"""

    select_dir: bool = True
    """是否开启选择目录功能"""

    select_file_button_text: str = "File"
    """选择文件按钮文本"""

    select_dir_button_text: str = "Directory"
    """选择目录按钮文本"""

    cancel_button_text: str = "Cancel"
    """取消按钮文本"""

    confirm_button_text: str = "Confirm"
    """确认按钮文本"""

    file_dialog_title: str = "Select File"
    """文件对话框标题"""

    dir_dialog_title: str = "Select Directory"
    """目录对话框标题"""

    file_filters: str = ""
    """文件过滤器"""

    start_dir: str = ""
    """起始路径"""


class PathEditDialog(QDialog):
    def __init__(
        self,
        parent: QWidget,
        current_value: str,
        config: Optional[PathEditDialogConfig] = None,
    ):
        super().__init__(parent)

        self._config = config or PathEditDialogConfig()
        self._current_value = current_value

        self.setWindowTitle(self._config.title)
        self.setModal(True)
        self.resize(450, 150)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._path_edit = QLineEdit(self)
        self._path_edit.setText(current_value)
        layout.addWidget(self._path_edit)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        if self._config.select_file:
            self._add_file_button = QPushButton(
                self._config.select_file_button_text, self
            )
            # noinspection PyUnresolvedReferences
            self._add_file_button.clicked.connect(self._on_add_file)
            button_layout.addWidget(self._add_file_button)

        if self._config.select_dir:
            self._add_dir_button = QPushButton(
                self._config.select_dir_button_text, self
            )
            # noinspection PyUnresolvedReferences
            self._add_dir_button.clicked.connect(self._on_add_dir)
            button_layout.addWidget(self._add_dir_button)

        self._confirm_button = QPushButton(self._config.confirm_button_text, self)
        # noinspection PyUnresolvedReferences
        self._confirm_button.clicked.connect(self._on_confirm)
        button_layout.addWidget(self._confirm_button)

        self._cancel_button = QPushButton(self._config.cancel_button_text, self)
        # noinspection PyUnresolvedReferences
        self._cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self._cancel_button)

        layout.addLayout(button_layout)
        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        )

    def _on_add_file(self):
        file_path = utils.get_open_file(
            self,
            self._file_dialog_title,
            self._start_dir,
            self._file_filters,
        )
        if not file_path:
            return
        self._path_edit.setText(file_path)

    def _on_add_dir(self):
        dir_path = utils.get_existing_directory(
            self,
            self._dir_dialog_title,
            self._start_dir,
        )
        if not dir_path:
            return
        self._path_edit.setText(dir_path)

    def _on_confirm(self):
        self._current_value = self._path_edit.text()
        self.accept()

    @property
    def current_value(self) -> str:
        return self._current_value


@dataclasses.dataclass(frozen=True)
class PathListEditConfig(CommonParameterWidgetConfig):
    """PathListEdit的配置类。"""

    default_value: Optional[List[str]] = dataclasses.field(default_factory=list)
    """默认值"""

    empty_string_strategy: Literal["keep_all", "keep_one", "remove_all"] = "remove_all"
    """对待列表中空字符串的策略，keep_all表示保留所有空字符串，keep_one表示只保留第一个空字符串，remove_all表示删除所有空字符串"""

    add_files: bool = True
    """是否开启添加文件路径功能"""

    add_dirs: bool = True
    """是否开启添加文件夹路径功能"""

    file_filters: str = ""
    """文件过滤器，用于文件对话框"""

    start_dir: str = ""
    """起始路径，用于文件对话框"""

    normalize_path: bool = True
    """是否将路径规范化"""

    absolutize_path: bool = True
    """是否将路径转换为绝对路径"""

    add_file_button_text: str = "Add Files"
    """添加文件按钮文本"""

    add_dir_button_text: str = "Add Dir"
    """添加目录按钮的文本"""

    remove_button_text: str = "Remove"
    """删除按钮文本"""

    clear_button_text: str = "Clear"
    """清空全部按钮文本"""

    file_dialog_title: str = "Select File"
    """添加文件对话框标题"""

    dir_dialog_title: str = "Select Directory"
    """添加文件夹对话框标题"""

    confirm_dialog_title: str = "Confirm"
    """确认对话框标题"""

    warning_dialog_title: str = "Warning"
    """警告对话框标题"""

    confirm_remove: bool = True
    """是否显示移除确认对话框"""

    confirm_clear: bool = True
    """是否显示清空确认对话框"""

    remove_confirm_message: str = "Are you sure to remove the selected item?"
    """移除确认对话框消息"""

    clear_confirm_message: str = "Are you sure to remove all items?"
    """清空确认对话框消息"""

    no_selection_message: str = "No items are selected!"
    """未选择任何项的提示"""

    drag_enabled: bool = True
    """是否允许拖拽"""

    wrapping: bool = False
    """是否允许换行"""

    text_elide_mode: Optional[TextElideMode] = None
    """文本省略模式"""

    alternating_row_colors: bool = True
    """是否使用交替行颜色"""

    width: Optional[int] = None
    """表格的最小宽度"""

    height: Optional[int] = 210
    """表格的最小高度"""

    drag_n_drop: bool = True
    """是否允许拖拽文件或目录到表格"""

    drag_n_drop_filter: Optional[Callable[[str, str], bool]] = default_dnd_filter
    """文件拖放功能的过滤函数。该函数应接收两个参数：文件过滤器（即本类的`filters`属性）和拖放的文件路径。
    若返回True，则表示该文件可以被拖放；否则，则表示该文件不能被拖放。该属性也可以设置为None，表示不对拖放文件进行过滤。
    默认情况下，使用`default_dnd_filter`函数作为过滤函数，该函数会将待拖放的文件的文件名与文件过滤器进行匹配，若命中任意文件过滤器，则返回True，
    否则返回False。比如，若文件过滤器为'Text files (*.txt);;Python files (*.py)', 则文件'hello.txt'可以被拖放，因为其命中了'Text files (*.txt)';
    文件'hello.py'也可以被拖放，因为其命中了'Python files (*.py)'；文件'hello.png'则不能被拖放，因为其没有命中任何文件过滤器。"""

    path_edit_dialog_config: Optional[PathEditDialogConfig] = None
    """编辑路径对话框的配置"""

    @classmethod
    def target_widget_class(cls) -> Type["PathListEdit"]:
        return PathListEdit


class PathListEdit(CommonParameterWidget):
    ConfigClass = PathListEditConfig

    ElideLeft = TextElideMode.ElideLeft
    """文本省略模式：省略左边"""

    ElideMiddle = TextElideMode.ElideMiddle
    """文本省略模式：省略中间"""

    ElideRight = TextElideMode.ElideRight
    """文本省略模式：省略右边"""

    ElideNone = TextElideMode.ElideNone
    """文本省略模式：不省略"""

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: PathListEditConfig,
    ):
        self._value_widget: Optional[QWidget] = None
        self._list_view: Optional[QListView] = None
        self._add_files_button: Optional[QPushButton] = None
        self._add_dirs_button: Optional[QPushButton] = None
        self._remove_button: Optional[QPushButton] = None
        self._clear_button: Optional[QPushButton] = None

        self._model: Optional[QStringListModel] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: PathListEditConfig
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            layout_main = QVBoxLayout()
            layout_main.setContentsMargins(0, 0, 0, 0)
            layout_main.setSpacing(0)
            self._value_widget.setLayout(layout_main)

            self._list_view = QListView(self._value_widget)
            if self._config.height is not None and self._config.height > 0:
                self._list_view.setMinimumHeight(self._config.height)

            if self._config.width is not None and self._config.width > 0:
                self._list_view.setMinimumWidth(self._config.width)

            if self._config.drag_enabled:
                self._list_view.setDragDropMode(QListView.InternalMove)
                self._list_view.setDefaultDropAction(Qt.DropAction.TargetMoveAction)
                self._list_view.setDragDropOverwriteMode(False)

            self._list_view.setWrapping(self._config.wrapping)

            if self._config.text_elide_mode is not None:
                self._list_view.setTextElideMode(self._config.text_elide_mode)
                if self._config.text_elide_mode == TextElideMode.ElideNone:
                    self._list_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                else:
                    self._list_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            else:
                self._list_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            self._list_view.setAlternatingRowColors(self._config.alternating_row_colors)

            self._model = QStringListModel(self._value_widget)
            self._list_view.setModel(self._model)
            layout_main.addWidget(self._list_view)

            layout_buttons = QGridLayout()
            layout_buttons.setSpacing(2)

            col_span = 1
            if not self._config.add_files or not self._config.add_dirs:
                col_span = 2

            add_dir_col = 1
            if not self._config.add_files:
                add_dir_col = 0

            if self._config.add_files:
                self._add_files_button = QPushButton(self._value_widget)
                self._add_files_button.setText(self._config.add_file_button_text)
                # noinspection PyUnresolvedReferences
                self._add_files_button.clicked.connect(self._on_add_files)
                layout_buttons.addWidget(self._add_files_button, 0, 0, 1, col_span)

            if self._config.add_dirs:
                self._add_dirs_button = QPushButton(self._value_widget)
                self._add_dirs_button.setText(self._config.add_dir_button_text)
                # noinspection PyUnresolvedReferences
                self._add_dirs_button.clicked.connect(self._on_add_dirs)
                layout_buttons.addWidget(
                    self._add_dirs_button, 0, add_dir_col, 1, col_span
                )

            self._remove_button = QPushButton(self._value_widget)
            self._remove_button.setText(self._config.remove_button_text)
            # noinspection PyUnresolvedReferences
            self._remove_button.clicked.connect(self._on_remove_item)
            layout_buttons.addWidget(self._remove_button, 1, 0)

            self._clear_button = QPushButton(self._value_widget)
            # noinspection PyUnresolvedReferences
            self._clear_button.clicked.connect(self._on_clear_items)
            self._clear_button.setText(self._config.clear_button_text)
            layout_buttons.addWidget(self._clear_button, 1, 1)

            self._list_view.setEditTriggers(QListView.NoEditTriggers)
            # noinspection PyUnresolvedReferences
            self._list_view.doubleClicked.connect(self._on_double_clicked)

            layout_main.addLayout(layout_buttons)
        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (list,), allow_none=True)

    def set_value_to_widget(self, value: List[str]):
        self._clear_items()
        self._append_items(value)

    def get_value_from_widget(self) -> List[str]:
        self._config: PathListEditConfig
        string_list = self._model.stringList()
        if self._config.empty_string_strategy == "keep_all":
            return [str(item) for item in string_list]
        elif self._config.empty_string_strategy == "keep_one":
            return self._keep_one_empty_item(string_list)
        else:
            return [str(item) for item in string_list if item != "" or item is not None]

    def on_drag(self, mime_data: QMimeData) -> bool:
        if not mime_data.hasUrls():
            return False
        if not mime_data.hasUrls():
            return False
        return True

    def on_drop(self, urls: List[QUrl], mime_data: QMimeData):
        self._config: PathListEditConfig
        if not urls:
            return
        paths = [
            f
            for f in (url.toLocalFile() for url in urls)
            if (
                self._config.drag_n_drop_filter is None
                or self._config.drag_n_drop_filter(self._config.file_filters, f) is True
            )
        ]
        if not paths:
            return
        self._append_items(paths)

    def _on_remove_item(self):
        self._config: PathListEditConfig
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
                buttons=utils.Yes | utils.No,
            )
            if ret == utils.No:
                return
        for index in selected:
            self._model.removeRow(index.row())

    def _on_clear_items(self):
        self._config: PathListEditConfig
        count = self._model.rowCount()
        if count <= 0:
            return
        if self._config.confirm_remove:
            ret = utils.show_question_message(
                self,
                message=self._config.clear_confirm_message,
                title=self._config.warning_dialog_title,
                buttons=utils.Yes | utils.No,
            )
            if ret == utils.No:
                return
        self._clear_items()

    def _on_add_files(self):
        self._config: PathListEditConfig
        paths = utils.get_open_files(
            self,
            title=self._config.file_dialog_title,
            start_dir=self._config.start_dir,
            filters=self._config.file_filters,
        )
        if not paths:
            return
        for path in paths:
            self._append_item(path, edit=False, set_current=True)

    def _on_add_dirs(self):
        self._config: PathListEditConfig
        path = utils.get_existing_directory(
            self,
            title=self._config.file_dialog_title,
            start_dir=self._config.start_dir,
        )
        if not path:
            return
        self._append_item(path, edit=False, set_current=True)

    def _clear_items(self):
        self._model.removeRows(0, self._model.rowCount())
        self._model.setStringList([])

    def _append_item(self, item: str, edit: bool = False, set_current: bool = False):
        self._config: PathListEditConfig
        if item is None:
            item = ""

        if item != "":
            if self._config.normalize_path:
                item = os.path.normpath(item)
            if self._config.absolutize_path:
                item = os.path.abspath(item)

        row = self._model.rowCount()
        self._model.insertRow(row)
        self._model.setData(self._model.index(row), str(item))
        # How to add a tooltip to each item?
        # It is very confusing why this need is not mentioned in the Qt documentation.
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
            if item is None:
                item = ""
            item = str(item)
            if item != "":
                ret.append(item)
                continue
            # if item == "" and
            if should_add:
                ret.append(item)
                should_add = False
        return ret

    def _on_double_clicked(self, index: QModelIndex):
        self._config: PathListEditConfig
        if not index or not index.isValid():
            return
        current_value = self._model.data(index, Qt.DisplayRole)

        if self._config.path_edit_dialog_config is None:
            dialog_config = PathEditDialogConfig(
                select_dir=self._config.add_dirs,
                select_file=self._config.add_files,
                file_filters=self._config.file_filters,
                start_dir=self._config.start_dir,
            )
        else:
            dialog_config = self._config.path_edit_dialog_config

        edit_dialog = PathEditDialog(
            self, current_value=current_value, config=dialog_config
        )
        ret = edit_dialog.exec_()
        if ret == QDialog.Accepted:
            new_value = edit_dialog.current_value
            if new_value != current_value:
                if self._config.normalize_path:
                    new_value = os.path.normpath(new_value)
                if self._config.absolutize_path:
                    new_value = os.path.abspath(new_value)
                self._model.setData(index, new_value)
        edit_dialog.deleteLater()
        del edit_dialog


class FileListEdit(PathListEdit):
    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: PathListEditConfig
    ):
        config = dataclasses.replace(config, add_files=True, add_dirs=False)
        super().__init__(parent, parameter_name, config)


def _is_directory(_: str, path: str) -> bool:
    return os.path.isdir(path)


class DirectoryListEdit(PathListEdit):
    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: PathListEditConfig
    ):
        config = dataclasses.replace(
            config, add_files=False, add_dirs=True, drag_n_drop_filter=_is_directory
        )
        super().__init__(parent, parameter_name, config)
