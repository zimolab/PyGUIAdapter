import dataclasses
from typing import Any, Dict, Type, Optional, List, Tuple, Union

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QCommandLinkButton, QDialog, QHeaderView

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...itemseditor.multiobject_editor import (
    NO_OBJECT_SELECTED_WARNING_MESSAGE,
    NO_OBJECT_ADDED_WARNING_MESSAGE,
    REMOVE_CONFIRM_MESSAGE,
    CLEAR_CONFIRM_MESSAGE,
    MULTIPLE_OBJECTS_WARNING_MESSAGE,
    MultiObjectEditorConfig,
    MultiObjectEditor,
    ObjectItemEditor,
)
from ...itemseditor.schema import ValueType
from ...utils import (
    show_critical_message,
    normalize_schema_object,
    validate_schema_object,
)


@dataclasses.dataclass(frozen=True)
class SchemaObjectsEditorConfig(CommonParameterWidgetConfig):
    default_value: Optional[List[Dict[str, Any]]] = None
    schema: Dict[str, ValueType] = None
    ignore_unknown_keys: bool = False
    fill_missing_keys: bool = False
    display_text: str = "Edit - {object_count} objects in list"
    window_title: str = "Objects Editor"
    window_size: Tuple[int, int] = (800, 600)
    center_container_title: str = ""
    item_editor_title: str = ""
    item_editor_size: Tuple[int, int] = (500, 600)
    item_editor_center_container_title: str = ""
    wrap_movement: bool = False
    add_button_text: str = "Add"
    edit_button_text: str = "Edit"
    remove_button_text: str = "Remove"
    clear_button_text: str = "Clear"
    move_up_button_text: str = "Move Up"
    move_down_button_text: str = "Move Down"
    stretch_last_section: bool = True
    no_selection_warning_message: Optional[str] = NO_OBJECT_SELECTED_WARNING_MESSAGE
    no_items_warning_message: Optional[str] = NO_OBJECT_ADDED_WARNING_MESSAGE
    remove_confirm_message: Optional[str] = REMOVE_CONFIRM_MESSAGE
    clear_confirm_message: Optional[str] = CLEAR_CONFIRM_MESSAGE
    multiple_selection_warning_message: Optional[str] = MULTIPLE_OBJECTS_WARNING_MESSAGE
    double_click_to_edit: bool = False
    resize_rows_to_contents: bool = True
    alternating_row_colors: bool = False
    show_horizontal_header: bool = True
    show_vertical_header: bool = True
    show_grid: bool = True
    continuous_selection: bool = True
    item_text_alignment: Union[int, Qt.AlignmentFlag, None] = None
    item_data_as_tooltip: bool = False
    item_data_as_status_tip: bool = False
    column_widths: Optional[Dict[int, int]] = None
    horizontal_resize_modes: Union[
        Dict[int, QHeaderView.ResizeMode], QHeaderView.ResizeMode, None
    ] = None
    vertical_resize_modes: Union[
        Dict[int, QHeaderView.ResizeMode], QHeaderView.ResizeMode, None
    ] = None

    @classmethod
    def target_widget_class(cls) -> Type["SchemaObjectsEditor"]:
        return SchemaObjectsEditor


class SchemaObjectsEditor(CommonParameterWidget):

    ConfigClass = SchemaObjectsEditorConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: SchemaObjectsEditorConfig,
    ):
        if not config.schema:
            raise ValueError("object schema is not provided")

        if not isinstance(config.default_value, (type(None), list)):
            raise TypeError(
                f"default_value of {parameter_name} should be a list, but got {type(config.default_value)}"
            )

        if config.default_value is not None:
            default_value = self._normalize_all(
                config, config.default_value, copy_object=True
            )
            config = dataclasses.replace(config, default_value=default_value)

        self._value_widget: Optional[QCommandLinkButton] = None
        self._current_value: List[Dict[str, Any]] = config.default_value or []

        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if not self._value_widget:
            self._value_widget = QCommandLinkButton(self)
            self._value_widget.setText(self.config.display_text)
            # noinspection PyUnresolvedReferences
            self._value_widget.clicked.connect(self._on_edit)
        return self._value_widget

    def check_value_type(self, value: List[Dict[str, Any]]):
        if not isinstance(value, (list, type(None))):
            raise TypeError(
                f"Value of {self.parameter_name} should be a list, but got {type(value)}"
            )
        self._validate_all(value, self.config)

    def set_value_to_widget(self, value: List[Dict[str, Any]]) -> None:
        del self._current_value[:]
        self._current_value = value
        self._update_display_text()

    def get_value_from_widget(self) -> List[Dict[str, Any]]:
        return self._current_value

    def _on_edit(self):
        config: SchemaObjectsEditorConfig = self.config
        editor_config = MultiObjectEditorConfig(
            ignore_unknown_columns=config.ignore_unknown_keys,
            fill_missing_keys_with_default=config.fill_missing_keys,
            window_title=config.window_title,
            window_size=config.window_size,
            item_editor_title=config.item_editor_title,
            item_editor_size=config.item_editor_size,
            item_editor_center_container_title=config.item_editor_center_container_title,
            wrap_movement=config.wrap_movement,
            add_button_text=config.add_button_text,
            edit_button_text=config.edit_button_text,
            remove_button_text=config.remove_button_text,
            clear_button_text=config.clear_button_text,
            move_up_button_text=config.move_up_button_text,
            move_down_button_text=config.move_down_button_text,
            stretch_last_section=config.stretch_last_section,
            no_selection_warning_message=config.no_selection_warning_message,
            no_items_warning_message=config.no_items_warning_message,
            remove_confirm_message=config.remove_confirm_message,
            clear_confirm_message=config.clear_confirm_message,
            multiple_selection_warning_message=config.multiple_selection_warning_message,
            double_click_to_edit=config.double_click_to_edit,
            resize_rows_to_contents=config.resize_rows_to_contents,
            alternating_row_colors=config.alternating_row_colors,
            show_horizontal_header=config.show_horizontal_header,
            show_vertical_header=config.show_vertical_header,
            show_grid=config.show_grid,
            continuous_selection=config.continuous_selection,
            item_text_alignment=config.item_text_alignment,
            item_data_as_tooltip=config.item_data_as_tooltip,
            item_data_as_status_tip=config.item_data_as_status_tip,
            column_widths=config.column_widths,
            horizontal_resize_modes=config.horizontal_resize_modes,
            vertical_resize_modes=config.vertical_resize_modes,
            validate_added_object=True,
            center_container_title=config.center_container_title,
        )
        editor = MultiObjectEditor(
            self,
            config.schema,
            editor_config,
            accept_hook=self._before_editor_accept,
            item_editor_accept_hook=self._before_item_editor_accept,
        )
        editor.set_objects(self._current_value)
        ret = editor.exec_()
        if ret == QDialog.Accepted:
            self.set_value_to_widget(editor.get_objects())
        editor.deleteLater()

    def _before_editor_accept(
        self, object_editor: MultiObjectEditor, new_value: List[Dict[str, Any]]
    ) -> bool:
        try:
            self._validate_all(new_value, self.config)
        except Exception as e:
            show_critical_message(object_editor, str(e), title="Error")
            return False
        return True

    def _before_item_editor_accept(
        self, item_editor: ObjectItemEditor, new_value: Dict[str, Any]
    ) -> bool:
        try:
            validate_schema_object(
                self.config.schema,
                new_value,
                ignore_missing_keys=self.config.fill_missing_keys,
                ignore_unknown_keys=self.config.ignore_unknown_keys,
            )
        except Exception as e:
            show_critical_message(item_editor, str(e), title="Error")
            return False
        return True

    def _update_display_text(self):
        self.value_widget.setText(
            self.config.display_text.format(object_count=len(self._current_value))
        )

    @staticmethod
    def _validate_all(objects: List[Dict[str, Any]], config: SchemaObjectsEditorConfig):
        for obj in objects:
            validate_schema_object(
                config.schema,
                obj,
                ignore_unknown_keys=config.ignore_unknown_keys,
                ignore_missing_keys=config.fill_missing_keys,
            )

    @staticmethod
    def _normalize_all(
        config: SchemaObjectsEditorConfig,
        objects: List[Dict[str, Any]],
        copy_object: bool = True,
    ) -> List[Dict[str, Any]]:
        ret = []
        for obj in objects:
            normalized_obj = normalize_schema_object(
                config.schema,
                obj,
                copy=copy_object,
                fill_missing_keys=config.fill_missing_keys,
                ignore_unknown_keys=config.ignore_unknown_keys,
            )
            ret.append(normalized_obj)
        return ret
