import dataclasses

from PySide2.QtWidgets import QMessageBox
from qtpy.QtWidgets import QWidget, QCommandLinkButton
from typing import Dict, Optional, Tuple, Any, Type

from ....widgets.common import CommonParameterWidgetConfig, CommonParameterWidget
from .editor import StringDictEditor
from .itemdlg import StringDictItemDialogConfig


@dataclasses.dataclass(frozen=True)
class StringDictEditConfig(CommonParameterWidgetConfig):
    default_value: Dict[str, str] = dataclasses.field(default_factory=dict)
    display_button_text: str = "Edit({} items in total)"
    editor_title: str = ""
    editor_size: Optional[Tuple[int, int]] = None
    key_label: str = "Key"
    value_label: str = "Value"
    up_button_text: str = "Up"
    down_button_text: str = "Down"
    add_button_text: str = "New"
    edit_button_text: str = "Edit"
    remove_button_text: str = "Remove"
    clear_button_text: str = "Clear"
    remove_confirm_message: Optional[str] = "Are you sure to remove this item?"
    clear_confirm_message: Optional[str] = "Are you sure to clear all items?"
    no_selected_item_message: str = "No item is selected! Please select an item first!"
    no_items_added_message: str = "No items are added!"
    accept_changes_message: str = "Accept changes?"
    waring_dialog_title: str = "Warning"
    error_dialog_title: str = "Error"
    confirm_dialog_title: str = "Confirm"
    vertical_header: bool = True
    value_column_editable: bool = True
    double_click_to_edit: bool = True
    add_item_dialog_title: str = "Add Item"
    edit_item_dialog_title: str = "Edit Item"
    item_dialog_size: Optional[Tuple[int, int]] = None
    item_dialog_config: Optional[StringDictItemDialogConfig] = None

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
    def value_widget(self) -> QWidget:
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
        self._current_value = value
        self._update_value_widget()

    def get_value_from_widget(self) -> Dict[str, str]:
        return self._current_value.copy()

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
                self.set_value(editor.string_dict)
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
