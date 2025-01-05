import ast
import sys
from typing import Any, List, Optional, Union, Tuple

from pyqcodeeditor.QCodeEditor import QCodeEditor
from pyqcodeeditor.highlighters.QPythonHighlighter import QPythonHighlighter
from qtpy.QtCore import QModelIndex, QPoint, Qt
from qtpy.QtGui import QTextOption, QFont
from qtpy.QtWidgets import (
    QWidget,
    QMessageBox,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QDialog,
    QVBoxLayout,
    QTextBrowser,
)

from ..schema import ValueWidgetMixin, ValueType
from ..tableview import TableView
from ..utils import Widget, format_py_code
from ..item_editor import BaseItemEditor

WINDOW_TITLE = "Variant Editor"
WINDOW_SIZE = (600, 400)
CENTER_CONTAINER_TITLE = "Variant"
TEXT_FONT_SIZE = 14
TEXT_FONT_FAMILY = "Arial, Consolas, monospace"
FORMAT_BUTTON_TEXT = "Format"
VARIANT_EDITOR_BUTTON_TEXT = "Edit Variant"


class VariantEditBox(QWidget, ValueWidgetMixin):
    def __init__(
        self,
        parent: QWidget,
        default_value: Any,
        *args,
        editor_button_text: str,
        window_title: str,
        window_size: Optional[Tuple[int, int]],
        center_container_title: str,
        text_font_size: int,
        text_font_family: str,
        format_button_text: Optional[str],
        **kwargs,
    ):
        self._editor_button_text = editor_button_text
        self._window_title = window_title
        self._window_size = window_size
        self._center_container_title = center_container_title
        self._text_font_size = text_font_size
        self._text_font_family = text_font_family
        self._format_button_text = format_button_text
        self._value = None

        super().__init__(parent, *args, **kwargs)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._value_preview = QTextBrowser(self)
        self._value_preview.setLineWrapMode(QTextBrowser.WidgetWidth)
        self._value_preview.setWordWrapMode(QTextOption.WrapAnywhere)
        self._value_preview.setFontFamily(self._text_font_family)
        font: QFont = self._value_preview.font()
        font.setPixelSize(self._text_font_size)
        self._value_preview.setFont(font)

        self._layout.addWidget(self._value_preview)

        self._edit_button = QPushButton(self)
        self._edit_button.setText(self._editor_button_text)
        # noinspection PyUnresolvedReferences
        self._edit_button.clicked.connect(self._on_edit_button_clicked)
        self._layout.addWidget(self._edit_button)

        self.set_value(default_value)

    def set_value(self, value: Any):
        self._value = value
        self._update_text()

    def get_value(self) -> Any:
        return self._value

    def on_create_variant_editor(self, **kwargs) -> "VariantEditor":
        return VariantEditor(self, self._value, **kwargs)

    def _update_text(self):
        text = repr(self._value)
        self._value_preview.setPlainText(text)

    def _on_edit_button_clicked(self):
        editor = self.on_create_variant_editor(
            window_title=self._window_title,
            window_size=self._window_size,
            center_container_title=self._center_container_title,
            text_font_size=self._text_font_size,
            text_font_family=self._text_font_family,
            format_button_text=self._format_button_text,
        )
        ret = editor.exec()
        if ret == QDialog.Accepted:
            self.set_value(editor.get_value())
        editor.deleteLater()


class VariantEditor(BaseItemEditor, ValueWidgetMixin):

    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: Any,
        *,
        window_title: str,
        window_size: Optional[Tuple[int, int]],
        center_container_title: str,
        text_font_size: int,
        text_font_family: str,
        format_button_text: Optional[str],
    ):
        self._text_font_size = text_font_size
        self._text_font_family = text_font_family
        self._format_button_text = format_button_text

        self._text_edit: Optional[QCodeEditor] = None
        self._format_button: Optional[QPushButton] = None

        self._value = None

        super().__init__(parent)

        self.setModal(True)

        if window_title:
            self.setWindowTitle(window_title)

        if window_size:
            self.resize(*window_size)

        if center_container_title:
            self.center_container.setTitle(center_container_title)
        flags = self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(flags)

        self.set_value(default_value)

    def user_bottom_widgets(self) -> List[Widget]:
        widgets = [QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)]
        if self._format_button_text:
            self._format_button = QPushButton()
            self._format_button.setText(self._format_button_text)
            # noinspection PyUnresolvedReferences
            self._format_button.clicked.connect(self._on_format_button_clicked)
            widgets.append(self._format_button)
        return widgets

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
            if self._text_font_size:
                self._text_edit.setFontSize(self._text_font_size)
            if self._text_font_family:
                self._text_edit.setFontFamily(self._text_font_family)
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

    def _on_format_button_clicked(self):
        cur_text = self._text_edit.toPlainText()
        if not cur_text:
            return
        try:
            formatted_text, changed = format_py_code(cur_text)
            if changed:
                self._text_edit.setPlainText(formatted_text.strip())
        except Exception as e:
            self.show_error_message("Error", str(e))


class VariantValue(ValueType):
    def __init__(
        self,
        default_value: Any,
        *,
        display_name: Optional[str] = None,
        window_title: str = WINDOW_TITLE,
        window_size: Optional[Tuple[int, int]] = WINDOW_SIZE,
        center_container_title: str = CENTER_CONTAINER_TITLE,
        text_font_size: int = TEXT_FONT_SIZE,
        text_font_family: str = TEXT_FONT_FAMILY,
        format_button_text: Optional[str] = FORMAT_BUTTON_TEXT,
        editor_button_text: Optional[str] = VARIANT_EDITOR_BUTTON_TEXT,
    ):

        self.window_title = window_title
        self.window_size = window_size
        self.center_container_title = center_container_title
        self.text_font_size = text_font_size
        self.text_font_family = text_font_family
        self.format_button_text = format_button_text
        self.editor_button_text = editor_button_text

        super().__init__(default_value, display_name=display_name)

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        try:
            _ = ast.literal_eval(repr(value))
            return True
        except Exception as e:
            print(f"invalid variant value {value}: {e}", file=sys.stderr)
            return False

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> VariantEditBox:
        return VariantEditBox(
            parent,
            self.default_value,
            editor_button_text=self.editor_button_text,
            window_title=self.window_title,
            window_size=self.window_size,
            center_container_title=self.center_container_title,
            text_font_size=self.text_font_size,
            text_font_family=self.text_font_family,
            format_button_text=self.format_button_text,
        )

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> VariantEditor:
        return VariantEditor(
            parent,
            self.default_value,
            window_title=self.window_title,
            window_size=self.window_size,
            center_container_title=self.center_container_title,
            text_font_size=self.text_font_size,
            text_font_family=self.text_font_family,
            format_button_text=self.format_button_text,
        )

    def before_set_editor_data(
        self,
        parent: TableView,
        editor: Union[QWidget, ValueWidgetMixin],
        index: QModelIndex,
    ):
        _ = index  # unused
        if not isinstance(editor, VariantEditor):
            return
        if self.window_size:
            editor.resize(*self.window_size)
        global_pos = parent.mapToGlobal(QPoint(0, 0))
        editor.move(
            global_pos.x() + (parent.width() - editor.width()) // 3,
            global_pos.y() + (parent.height() - editor.height()) // 3,
        )
