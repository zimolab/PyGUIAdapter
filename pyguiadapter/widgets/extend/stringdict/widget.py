import dataclasses

from qtpy.QtWidgets import QWidget, QCommandLinkButton, QMessageBox
from typing import Dict, Optional, Tuple, Any, Type

from ....widgets.common import CommonParameterWidgetConfig, CommonParameterWidget
from .editor import StringDictEditor
from .itemdlg import StringDictItemEditorConfig


@dataclasses.dataclass(frozen=True)
class StringDictEditConfig(CommonParameterWidgetConfig):
    default_value: Dict[str, str] = dataclasses.field(default_factory=dict)
    """默认值"""

    display_button_text: str = "Edit({} items in total)"
    """在编辑按钮上显示的文本，其中{}会被替换为当前字典的长度"""

    editor_title: str = ""
    """字典编辑器的标题"""

    editor_size: Optional[Tuple[int, int]] = None
    """字典编辑器的窗口大小"""

    key_label: str = "Key"
    """字典编辑器中key列的名称"""

    value_label: str = "Value"
    """字典编辑器中value列的名称"""

    up_button_text: str = "Up"
    """字典编辑器中向上按钮的文本"""

    down_button_text: str = "Down"
    """字典编辑器中向下按钮的文本"""

    add_button_text: str = "New"
    """字典编辑器中添加按钮的文本"""

    edit_button_text: str = "Edit"
    """字典编辑器中编辑按钮的文本"""

    remove_button_text: str = "Remove"
    """字典编辑器中移除按钮的文本"""

    clear_button_text: str = "Clear"
    """字典编辑器中清空按钮的文本"""

    remove_confirm_message: Optional[str] = "Are you sure to remove this item?"
    """从字典编辑器中移除字典项时弹出的确认对话框的消息"""

    clear_confirm_message: Optional[str] = "Are you sure to clear all items?"
    """从字典编辑器中清空字典项时弹出的确认对话框的消息"""

    no_selected_item_message: str = "No item is selected! Please select an item first!"
    """从字典编辑器中移除或编辑字典项时，没有选中任何项时的提示信息"""

    no_items_added_message: str = "No items are added!"
    """从字典编辑器中清除字典项，如果没有添加任何项时的提示信息"""

    accept_changes_message: str = "Accept changes?"
    """字典编辑器中关闭时弹出的确认对话框的消息"""

    waring_dialog_title: str = "Warning"
    """警告对话框的标题"""

    error_dialog_title: str = "Error"
    """错误对话框的标题"""

    confirm_dialog_title: str = "Confirm"
    """确认对话框的标题"""

    vertical_header: bool = True
    """是否显示垂直表头，垂直表头一般用于显示序号"""

    value_column_editable: bool = True
    """是否允许原地编辑value列"""

    double_click_to_edit: bool = True
    """是否允许双击单元格来编辑当前项"""

    add_item_editor_title: str = "Add Item"
    """添加字典项对话框的标题"""

    edit_item_editor_title: str = "Edit Item"
    """编辑字典项对话框的标题"""

    item_editor_size: Optional[Tuple[int, int]] = None
    """字典项编辑器的窗口大小"""

    item_editor_config: Optional[StringDictItemEditorConfig] = None
    """字典项编辑器的配置"""

    def target_widget_class(self) -> Type["StringDictEdit"]:
        return StringDictEdit


class StringDictEdit(CommonParameterWidget):
    ConfigClass = StringDictEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: StringDictEditConfig,
    ):
        self._value_widget: Optional[QCommandLinkButton] = None
        self._current_value: Dict[str, str] = {}
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QCommandLinkButton:
        if not self._value_widget:
            self._value_widget = QCommandLinkButton(self)
            self._value_widget.clicked.connect(self._on_edit)

        return self._value_widget

    def check_value_type(self, value: Any):
        if value is not None and not isinstance(value, dict):
            raise TypeError(
                f"Value of {self.parameter_name} should be a dict, but got {type(value)}"
            )

    def set_value_to_widget(self, value: Dict[str, str]) -> None:
        self._current_value.clear()
        # self._current_value.update(value)
        self._current_value = value
        self._update_value_widget()

    def get_value_from_widget(self) -> Dict[str, str]:
        return self._current_value

    def _update_value_widget(self):
        display_text = self.config.display_button_text.format(len(self._current_value))
        self._value_widget.setText(display_text)

    def _on_edit(self):
        editor_config = dataclasses.asdict(self.config)
        editor_config.pop("default_value")
        editor_config.pop("display_button_text")
        editor_config.pop("editor_title")
        editor_config.pop("editor_size")
        editor_config.pop("accept_changes_message")

        def before_close(editor_: StringDictEditor) -> bool:
            ret = QMessageBox.question(
                editor_,
                self.config.confirm_dialog_title,
                self.config.accept_changes_message,
                QMessageBox.Yes | QMessageBox.No,
            )
            if ret == QMessageBox.Yes:
                self.set_value_to_widget(editor_.string_dict)
            return True

        editor = StringDictEditor(
            self,
            title=self.config.editor_title,
            size=self.config.editor_size,
            before_close_callback=before_close,
            **editor_config,
        )
        editor.string_dict = self.get_value()
        editor.exec_()
        editor.destroy()
        editor.deleteLater()
