import dataclasses
from typing import Any, Dict, Type, Optional, Union, Tuple

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QCommandLinkButton, QDialog

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...itemseditor import ObjectEditor, ObjectEditorConfig
from ...itemseditor.schema import ValueType, make_default
from ...utils import (
    show_critical_message,
    validate_schema_object,
    normalize_schema_object,
)


@dataclasses.dataclass(frozen=True)
class SchemaObjectEditorConfig(CommonParameterWidgetConfig):
    default_value: Optional[Dict[str, Any]] = None
    schema: Dict[str, ValueType] = None
    ignore_unknown_keys: bool = False
    fill_missing_keys: bool = False
    display_text: str = "Edit"
    window_title: str = "Object Editor"
    window_size: Tuple[int, int] = (500, 600)
    center_container_title: str = ""
    key_column_header: str = "Key"
    value_column_header: str = "Value"
    item_text_alignment: Union[Qt.AlignmentFlag, int, None] = Qt.AlignCenter
    value_item_alignment: Union[Qt.AlignmentFlag, int, None] = None
    key_item_selectable: bool = False
    row_selection_mode: bool = True
    real_key_as_tooltip: bool = False
    stretch_last_section: bool = True
    alternating_row_colors: bool = False
    show_vertical_header: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["SchemaObjectEditor"]:
        return SchemaObjectEditor


class SchemaObjectEditor(CommonParameterWidget):

    ConfigClass = SchemaObjectEditorConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: SchemaObjectEditorConfig,
    ):
        if not config.schema:
            raise ValueError("object schema is not provided")

        if not isinstance(config.default_value, (type(None), dict)):
            raise TypeError(
                f"default_value of {parameter_name} should be a dict, but got {type(config.default_value)}"
            )

        if config.default_value is not None:
            default_value = normalize_schema_object(
                config.schema,
                config.default_value,
                copy=True,
                fill_missing_keys=config.fill_missing_keys,
                ignore_unknown_keys=config.ignore_unknown_keys,
            )
            config = dataclasses.replace(config, default_value=default_value)

        self._value_widget: Optional[QCommandLinkButton] = None
        self._current_value: Dict[str, Any] = config.default_value or make_default(
            config.schema
        )

        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if not self._value_widget:
            self._value_widget = QCommandLinkButton(self)
            self._value_widget.setText(self.config.display_text)
            # noinspection PyUnresolvedReferences
            self._value_widget.clicked.connect(self._on_edit)
        return self._value_widget

    def check_value_type(self, value: Any):
        self.validate_value(value, self.config)

    def set_value_to_widget(self, value: Dict[str, Any]) -> None:
        del self._current_value
        self._current_value = value

    def get_value_from_widget(self) -> Dict[str, Any]:
        return self._current_value

    def _on_edit(self):
        config: SchemaObjectEditorConfig = self.config
        editor_config = ObjectEditorConfig(
            ignore_unknown_columns=config.ignore_unknown_keys,
            window_title=config.window_title,
            window_size=config.window_size,
            key_column_header=config.key_column_header,
            value_column_header=config.value_column_header,
            item_text_alignment=config.item_text_alignment,
            value_item_alignment=config.value_item_alignment,
            key_item_selectable=config.key_item_selectable,
            row_selection_mode=config.row_selection_mode,
            real_key_as_tooltip=config.real_key_as_tooltip,
            alternating_row_colors=config.alternating_row_colors,
            show_vertical_header=config.show_vertical_header,
            stretch_last_section=config.stretch_last_section,
            ignore_unknown_keys=config.ignore_unknown_keys,
            center_container_title=config.center_container_title,
        )
        object_editor = ObjectEditor(
            self, config.schema, editor_config, accept_hook=self._before_editor_accept
        )
        object_editor.set_object(self._current_value, normalize=False, copy=False)
        ret = object_editor.exec_()
        if ret == QDialog.Accepted:
            self.set_value_to_widget(object_editor.get_object())
        object_editor.deleteLater()

    def _before_editor_accept(
        self, object_editor: ObjectEditor, new_value: Dict[str, Any]
    ) -> bool:
        try:
            self.validate_value(new_value, self.config)
        except Exception as e:
            show_critical_message(object_editor, str(e), title="Error")
            return False
        return True

    @staticmethod
    def validate_value(value: Dict[str, Any], config: SchemaObjectEditorConfig):
        if value is None:
            return
        validate_schema_object(
            config.schema,
            value,
            ignore_unknown_keys=config.ignore_unknown_keys,
            ignore_missing_keys=config.fill_missing_keys,
        )
