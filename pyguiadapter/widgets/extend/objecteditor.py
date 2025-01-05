import dataclasses
from typing import Any, Dict, Type, Optional

from qtpy.QtWidgets import QWidget, QCommandLinkButton, QDialog

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ..itemseditor.object_editor import ObjectEditor, ObjectEditorConfig
from ..itemseditor.schema import (
    ValueType,
    ValidationResult,
    MissingKeysError,
    UnknownKeysError,
    validate_object,
    InvalidValueError,
    make_default,
    remove_unknown_keys,
    fill_missing_keys,
)
from ...utils import show_critical_message


@dataclasses.dataclass(frozen=True)
class SchemaObjectEditorConfig(CommonParameterWidgetConfig):
    default_value: Optional[Dict[str, Any]] = None
    schema: Dict[str, ValueType] = None
    ignore_unknown_keys: bool = False
    fill_missing_keys: bool = False
    display_text: str = "Edit"

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
                f"default_value of {parameter_name} should be a dict or None, but got {type(config.default_value)}"
            )

        if config.default_value is not None:
            default_value = {**config.default_value}
            if config.ignore_unknown_keys:
                default_value = remove_unknown_keys(
                    schema=config.schema, obj=default_value, copy=False
                )
            if config.fill_missing_keys:
                default_value = fill_missing_keys(
                    schema=config.schema, obj=default_value, copy=False
                )
            config = dataclasses.replace(config, default_value=default_value)
            self._validate_value(config.default_value, config)

        # print(config.default_value)

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
        self._validate_value(value, self.config)

    def set_value_to_widget(self, value: Dict[str, Any]) -> None:
        self._current_value.clear()
        self._current_value = value

    def get_value_from_widget(self) -> Dict[str, Any]:
        return self._current_value

    def _on_edit(self):
        editor_config = ObjectEditorConfig(
            ignore_unknown_columns=self.config.ignore_unknown_keys
        )
        object_editor = ObjectEditor(
            self,
            self.config.schema,
            editor_config,
            accept_hook=self._before_editor_accept,
        )
        object_editor.set_object(self._current_value)
        ret = object_editor.exec_()
        if ret == QDialog.Accepted:
            new_value = object_editor.get_object()
            self._current_value.update(new_value)
        object_editor.deleteLater()

    def _before_editor_accept(
        self, object_editor: ObjectEditor, new_value: Dict[str, Any]
    ) -> bool:
        try:
            self._validate_value(new_value, self.config)
        except Exception as e:
            show_critical_message(object_editor, str(e), title="Error")
            return False
        return True

    def _validate_value(self, value: Dict[str, Any], config: SchemaObjectEditorConfig):
        if value is None:
            return

        if not isinstance(value, dict):
            raise TypeError(
                f"Value of {self.parameter_name} should be a dict, but got {type(value)}"
            )

        value = {**value}

        if config.fill_missing_keys:
            value = fill_missing_keys(config.schema, value, copy=False)

        if config.ignore_unknown_keys:
            value = remove_unknown_keys(config.schema, value, copy=False)

        result_wrapper = validate_object(
            config.schema, value, ignore_unknown_keys=config.ignore_unknown_keys
        )
        result = result_wrapper.result
        if result == ValidationResult.Valid:
            return
        if result == ValidationResult.MissingKeys:
            missing_keys = result_wrapper.extra_info
            raise MissingKeysError(f"missing keys: {missing_keys}", missing_keys)
        if result == ValidationResult.UnknownKeys:
            unknown_keys = result_wrapper.extra_info
            raise UnknownKeysError(f"unknown keys: {unknown_keys}", unknown_keys)
        if result == ValidationResult.InvalidValue:
            key, value, vt = result_wrapper.extra_info
            raise InvalidValueError(f"invalid value: {key}: {value}", key, value, vt)
        raise ValueError(f"unknown validation result: {result}")
