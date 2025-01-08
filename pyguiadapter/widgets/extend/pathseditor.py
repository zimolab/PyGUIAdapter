import dataclasses
from typing import List, Optional, Tuple, Type, Any

from qtpy.QtWidgets import QWidget, QCommandLinkButton

from ...itemseditor.paths_editor import (
    PathsEditor as _PathsEditor,
    PathsEditorConfig as _PathsEditorConfig,
)
from ...widgets.common import CommonParameterWidgetConfig, CommonParameterWidget


@dataclasses.dataclass(frozen=True)
class PathsEditorConfig(CommonParameterWidgetConfig):
    default_value: List[str] = dataclasses.field(default_factory=list)

    editor_button_text: str = "Edit({} paths in list)"
    """编辑按钮的文本"""

    editor_title: str = ""
    """路径列表编辑器的标题"""

    editor_size: Tuple[int, int] = (750, 600)
    """路径列表编辑器窗口的大小"""

    file_list_title: str = "Paths"
    """路径列表区域的标题"""

    add_file: bool = True
    """是否开启添加文件功能"""

    add_dir: bool = True
    """是否开启添加文件夹功能"""

    add_file_button_text: str = "File..."
    """添加文件按钮的文本"""

    file_filters: str = ""
    """文件过滤器，用于选择文件对话框"""

    add_dir_button_text: str = "Folder..."
    """添加文件夹按钮的文本"""

    start_dir: str = ""
    """文件对话框的初始目录"""

    path_as_posix: bool = True
    """是否将选择的文件或文件夹的路径以 Posix 格式保存"""

    edit_button_text: str = "Edit"
    """编辑按钮的文本"""

    remove_button_text: str = "Remove"
    """移除按钮的文本"""

    clear_button_text: str = "Clear"
    """清空按钮的文本"""

    up_button_text: str = "Up"
    """上移按钮的文本"""

    down_button_text: str = "Down"
    """下移按钮的文本"""

    file_dialog_title: str = "Select File"
    """选择文件对话框的标题"""

    dir_dialog_title: str = "Select Directory"
    """选择文件夹对话框的标题"""

    confirm_dialog_title: str = "Confirm"
    """确认对话框的标题"""

    warning_dialog_title: str = "Warning"
    """警告对话框的标题"""

    confirm_clear_message: Optional[str] = "Remove all the paths from the list?"
    """清空文件列表的确认消息文本，如果为 None 则不显示确认消息，直接清空文件列表"""

    confirm_remove_message: Optional[str] = "Remove the selected path(s) from the list?"
    """移除当前选中项的确认消息文本，如果为 None 则不显示确认消息，直接移除当前选中项"""

    no_items_selected_message: Optional[str] = "No path selected!"
    """没有选中任何项时的提示消息"""

    no_items_added_message: Optional[str] = "No path added!"
    """没有添加任何项时的提示消息"""

    double_click_to_edit: bool = True
    """是否允许双击列表项进行编辑"""

    path_item_editor_title: str = "Edit Path"
    """路径编辑对话框的标题"""

    path_item_editor_center_container_title: str = "Path"
    """路径编辑对话框中中心容器的标题"""

    @classmethod
    def target_widget_config(cls) -> Type["PathsEditor"]:
        return PathsEditor


class PathsEditor(CommonParameterWidget):
    ConfigClass = PathsEditorConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: PathsEditorConfig,
    ):
        self._value_widget: Optional[QCommandLinkButton] = None
        self._current_value: List[str] = []
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        if not isinstance(value, list):
            raise TypeError(f"Value must be a list, but got {type(value)}")

    @property
    def value_widget(self) -> QCommandLinkButton:
        if not self._value_widget:
            self._value_widget = QCommandLinkButton(self)
            self._value_widget.setText(
                self.config.editor_button_text.format(len(self._current_value))
            )
            # noinspection PyUnresolvedReferences
            self._value_widget.clicked.connect(self._on_edit)
        return self._value_widget

    def set_value_to_widget(self, value: List[str]) -> None:
        self._current_value.clear()
        self._current_value = value
        self._update_value_widget()

    def get_value_from_widget(self) -> List[str]:
        return self._current_value

    def _on_edit(self):
        paths_editor = _PathsEditor(self, self._create_paths_editor_config())
        edited, ok = paths_editor.start(self._current_value)
        paths_editor.deleteLater()
        if not ok:
            return
        self.set_value_to_widget(edited)

    def _update_value_widget(self):

        editor_button_text = self.config.editor_button_text.format(
            len(self._current_value)
        )
        self._value_widget.setText(editor_button_text)

    def _create_paths_editor_config(self) -> _PathsEditorConfig:
        config: PathsEditorConfig = self.config
        add_file_button_text = config.add_file_button_text if config.add_file else None
        add_dir_button_text = config.add_dir_button_text if config.add_dir else None
        return _PathsEditorConfig(
            window_title=config.editor_title,
            window_size=config.editor_size,
            as_posix=config.path_as_posix,
            add_file_button_text=add_file_button_text,
            add_directory_button_text=add_dir_button_text,
            file_filters=config.file_filters,
            start_directory=config.start_dir,
            file_dialog_title=config.file_dialog_title,
            directory_dialog_title=config.dir_dialog_title,
            confirm_dialog_title=config.confirm_dialog_title,
            warning_dialog_title=config.warning_dialog_title,
            add_button_text=config.edit_button_text,
            remove_button_text=config.remove_button_text,
            clear_button_text=config.clear_button_text,
            move_up_button_text=config.up_button_text,
            move_down_button_text=config.down_button_text,
            clear_confirm_message=config.confirm_clear_message,
            remove_confirm_message=config.confirm_remove_message,
            no_selection_warning_message=config.no_items_selected_message,
            no_items_warning_message=config.no_items_added_message,
            double_click_to_edit=config.double_click_to_edit,
            center_container_title=config.file_list_title,
            item_editor_title=config.path_item_editor_title,
            item_editor_center_container_title=config.path_item_editor_center_container_title,
        )
