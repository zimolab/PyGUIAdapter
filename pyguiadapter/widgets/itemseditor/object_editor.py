import dataclasses
from typing import Tuple, Optional, Dict, Any, List, Callable

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog, QWidget, QVBoxLayout, QDialogButtonBox

from .common_config import CommonEditorConfig
from .itemsview_container import CommonItemsViewContainer
from .object_tableview import ObjectEditViewConfig, ObjectEditView
from .schema import ValueType


@dataclasses.dataclass
class ObjectEditorConfig(ObjectEditViewConfig, CommonEditorConfig):
    window_title: str = "Object Editor"
    window_size: Tuple[int, int] = (500, 600)
    stretch_last_section: bool = True
    ignore_unknown_columns: bool = True
    alternating_row_colors: bool = False
    show_vertical_header: bool = False
    key_item_selectable: bool = True


class ObjectEditor(QDialog):
    def __init__(
        self,
        parent: Optional[QWidget],
        schema: Dict[str, ValueType],
        config: ObjectEditorConfig,
        *,
        accept_hook: Optional[Callable[["ObjectEditor", Dict[str, Any]], bool]] = None,
        reject_hook: Optional[Callable[["ObjectEditor"], bool]] = None,
    ):
        self._schema = schema
        self._config = config
        self._accept_hook = accept_hook
        self._reject_hook = reject_hook

        super().__init__(parent)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._object_view = ObjectEditView(self, config, schema)
        self._view_container = CommonItemsViewContainer(
            self, self._object_view, control_button_hooks=self
        )
        self._layout.addWidget(self._view_container)

        self._setup_ui()

    def update_object(
        self, obj: Dict[str, Any], remove_unknown_keys: bool = True, copy: bool = True
    ):
        if copy:
            obj = obj.copy()
        if remove_unknown_keys:
            for key in self.unknown_keys(obj):
                del obj[key]
        self._object_view.update_object(obj)

    def set_object(
        self, obj: Dict[str, Any], normalize: bool = True, copy: bool = True
    ):
        obj = self.normalize_object(obj, copy) if normalize else obj
        self._object_view.update_object(obj)

    def get_object(self) -> Dict[str, Any]:
        return self._object_view.get_object()

    def missing_keys(self, obj: Dict[str, Any]) -> List[str]:
        missing_keys = []
        for key in self._schema.keys():
            if key not in obj:
                missing_keys.append(key)
        return missing_keys

    def unknown_keys(self, obj: Dict[str, Any]) -> List[str]:
        unknown_keys = []
        for key in obj.keys():
            if key not in self._schema:
                unknown_keys.append(key)
        return unknown_keys

    def validate_object(self, obj: Dict[str, Any]) -> bool:
        if self.missing_keys(obj):
            return False
        if self.unknown_keys(obj):
            return False
        for key, value in obj.items():
            if not self._schema[key].validate(value):
                return False
        return True

    def normalize_object(
        self, obj: Dict[str, Any], copy: bool = True
    ) -> Dict[str, Any]:
        if copy:
            obj = obj.copy()
        # remove unknown keys
        for key in self.unknown_keys(obj):
            del obj[key]
        # add missing keys with default values
        for key, value_type in self._schema.items():
            if key not in obj:
                obj[key] = value_type.default_value
        return obj

    def _setup_ui(self):
        self._view_container.hide_control_widgets_panel()
        if self._config.standard_buttons:
            self._dialog_button_box = QDialogButtonBox(self)
            self._dialog_button_box.setStandardButtons(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.accepted.connect(self.accept)
            # noinspection PyUnresolvedReferences
            self._dialog_button_box.rejected.connect(self.reject)
            self._layout.addWidget(self._dialog_button_box)

        if self._config.window_title:
            self.setWindowTitle(self._config.window_title)

        if self._config.window_size:
            self.resize(*self._config.window_size)

        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

    def accept(self):
        if self._accept_hook is None or self._accept_hook(self, self.get_object()):
            super().accept()
            return

    def reject(self):
        if self._reject_hook is None or self._reject_hook(self):
            super().reject()
            return
