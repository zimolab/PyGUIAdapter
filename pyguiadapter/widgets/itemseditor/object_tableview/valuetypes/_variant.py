import ast
import sys
from typing import Any, List, Optional, Union, Tuple

from qtpy.QtCore import QModelIndex, QPoint
from qtpy.QtWidgets import QWidget, QMessageBox
from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.highlighters.QPythonHighlighter import QPythonHighlighter

from ..schema import ValueWidgetMixin, ValueType
from ...tableview import TableView
from ...utils import Widget
from ....itemseditor.item_editor import BaseItemEditor


class VariantValueEditor(BaseItemEditor, ValueWidgetMixin):

    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: Any,
        *,
        window_title: str = "",
        window_size: Optional[Tuple[int, int]] = (500, 800),
        center_container_title: str = "",
    ):
        self._text_edit: Optional[QCodeEditor] = None

        self._value = None

        super().__init__(parent)

        self.setModal(True)

        if window_title:
            self.setWindowTitle(window_title)

        if window_size:
            print("resize", window_size)
            self.resize(*window_size)

        if center_container_title:
            self.center_container.setTitle(center_container_title)

        self.set_value(default_value)

    def user_bottom_widgets(self) -> List[Widget]:
        return []

    def set_data(self, data: str):
        self._text_edit.setPlainText(str(data))

    def get_data(self) -> str:
        return self._text_edit.toPlainText().strip()

    def set_value(self, value: Any):
        literal_str, valid = self.to_variant_literal(value)
        if not valid:
            return
        self._value = value
        return self.set_data(literal_str)

    def get_value(self) -> Any:
        return self._value

    def on_create_center_widget(self, parent: QWidget) -> QWidget:
        if self._text_edit is None:
            self._text_edit = QCodeEditor(parent)
            self._text_edit.setTabReplace(True)
            self._text_edit.setHighlighter(QPythonHighlighter())
            self._text_edit.setLineWrapMode(QCodeEditor.WidgetWidth)
        return self._text_edit

    def accept(self):
        variant_literal_str = self.get_data()
        value, valid = self.from_variant_literal(variant_literal_str)
        if not valid:
            return
        self._value = value
        super().accept()

    def reject(self):
        super().reject()

    def to_variant_literal(self, value: Any) -> Tuple[str, bool]:
        literal_str = repr(value)
        try:
            _ = ast.literal_eval(literal_str)
            return literal_str, True
        except Exception as e:
            self.show_error_message("Error", f"Invalid variant literal: {e}")
            return repr(self._value), False

    def from_variant_literal(self, variant_literal_str: str) -> Tuple[Any, bool]:
        try:
            return ast.literal_eval(variant_literal_str), True
        except Exception as e:
            self.show_error_message("Error", f"Invalid variant literal: {e}")
            return self._value, False

    def show_error_message(self, title: str, message: str):
        QMessageBox.warning(self, title, message)


class VariantValue(ValueType):
    def __init__(self, default_value: Any, *, display_name: Optional[str] = None):
        super().__init__(default_value, display_name=display_name)

    def validate(self, value: Any) -> bool:
        try:
            _ = ast.literal_eval(repr(value))
            return True
        except Exception as e:
            print(f"invalid variant value {value}: {e}", file=sys.stderr)
            return False

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin, None]:
        return None

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return VariantValueEditor(parent, self.default_value)

    def before_set_editor_data(
        self,
        parent: TableView,
        editor: Union[QWidget, ValueWidgetMixin],
        index: QModelIndex,
    ):
        _ = index  # unused
        if not isinstance(editor, VariantValueEditor):
            return
        global_pos = parent.mapToGlobal(QPoint(0, 0))
        editor.move(
            global_pos.x() + (parent.width() - editor.width()) // 3,
            global_pos.y() + (parent.height() - editor.height()) // 3,
        )
