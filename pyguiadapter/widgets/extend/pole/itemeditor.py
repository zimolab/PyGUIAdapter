import dataclasses
from typing import Optional, Tuple, Dict, Any

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QDialogButtonBox,
    QGridLayout,
    QSpacerItem,
)

from .valuetypes import ValueTypeBase, ValueWidgetMixin

_DEFAULT_SIZE = (620, 580)


@dataclasses.dataclass
class PlainObjectItemEditorConfig:
    object_schema: Dict[str, ValueTypeBase] = dataclasses.field(default_factory=dict)
    title: str = "Object Editor"
    size: Optional[Tuple[int, int]] = None
    edit_area_title: str = "Object"


class PlainObjectItemEditor(QDialog):
    def __init__(
        self, config: PlainObjectItemEditorConfig, parent: Optional[QWidget] = None
    ):
        if not config.object_schema:
            raise ValueError("schema cannot be empty")
        self._config = config
        super().__init__(parent)

        self._value_widgets: Dict[str, ValueWidgetMixin] = {}

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._edit_area = QGroupBox(self)
        self._edit_area.setTitle(self._config.edit_area_title)
        self._layout.addWidget(self._edit_area)

        self._edit_area_layout = QVBoxLayout()
        self._edit_area.setLayout(self._edit_area_layout)

        self._scrollarea = QScrollArea(self._edit_area)
        self._scrollarea.setWidgetResizable(True)
        self._scrollarea_content = QWidget(self._scrollarea)
        self._scrollarea.setWidget(self._scrollarea_content)
        self._scrollarea_content_layout = QGridLayout()
        self._scrollarea_content.setLayout(self._scrollarea_content_layout)
        self._create_object_form(
            self._scrollarea_content, self._scrollarea_content_layout
        )
        self._edit_area_layout.addWidget(self._scrollarea)

        self._dlg_button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        self._dlg_button_box.accepted.connect(self.accept)
        self._dlg_button_box.rejected.connect(self.reject)
        self._layout.addWidget(self._dlg_button_box)

        self.setWindowTitle(self._config.title)
        self.resize(*self._config.size or _DEFAULT_SIZE)

    def _create_object_form(self, parent: QWidget, content_layout: QGridLayout):
        row = 0
        for key, value_type in self._config.object_schema.items():
            key_label = QLabel(parent)
            key_label.setText(key)
            content_layout.addWidget(key_label, row, 0)
            value_widget = value_type.on_create_edit(parent)
            value_widget.setObjectName(self._value_widget_object_name(key))
            self._value_widgets[key] = value_widget
            content_layout.addWidget(value_widget, row, 1)
            row += 1
        content_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def set_object(self, obj: Dict[str, Any], ignore_unknown_keys: bool = False):
        for key, value in obj.items():
            value_widget = self._value_widgets.get(key, None)
            if value_widget is None or not isinstance(value_widget, ValueWidgetMixin):
                if ignore_unknown_keys:
                    continue
                raise ValueError(f"unknown key: {key}")
            value_widget.set_value(value)

    def get_object(self) -> Dict[str, Any]:
        result = {}
        for key, value_widget in self._value_widgets.items():
            result[key] = value_widget.get_value()
        return result

    def destroy(self, destroy_window: bool = True, destroy_children: bool = True):
        self._value_widgets.clear()
        del self._value_widgets
        super().destroy(destroy_window, destroy_children)

    # noinspection PyMethodMayBeStatic
    def _value_widget_object_name(self, key: str):
        return f"_value_widget_{key}"
