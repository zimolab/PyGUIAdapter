from typing import Optional, Any, Union, Tuple

from qtpy.QtCore import Qt, QPoint, QModelIndex
from qtpy.QtGui import QColor, QFont
from qtpy.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QColorDialog,
    QTableWidgetItem,
)

from .. import ObjectEditView
from ..schema import ValueType, ValueWidgetMixin
from ...tableview import TableView
from ...utils import is_valid_color, to_qcolor, get_inverted_color, convert_color

DEFAULT_VALUE = "#FFFFFF"
ALPHA_CHANNEL = False
DISPLAY_COLOR_NAME = True
WIDGET_BORDER = False
WIDGET_HEIGHT = 35


ColorType = Union[
    Tuple[int, int, int, int],  # RGB
    Tuple[int, int, int],  # RGBA
    str,  # color name or hex
    QColor,
    list,  # will be converted to a tuple
]


class ColorLabel(QLabel):
    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: ColorType,
        *,
        alpha_channel: bool,
        display_color_name: bool,
        border: bool,
    ):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        if border:
            self.setFrameShape(QFrame.Box)
            self.setFrameShadow(QFrame.Raised)

        font: QFont = self.font()
        font.setBold(True)
        self.setFont(font)

        self._color = None
        self._alpha_channel = alpha_channel
        self._display_color_name = display_color_name

        self.set_value(default_value)

    def set_value(self, color: ColorType):
        self._color = to_qcolor(color)
        self._update_ui()

    def get_value(self) -> str:
        # noinspection PyTypeChecker
        return convert_color(self._color, "str", self._alpha_channel)

    def mouseReleaseEvent(self, ev):
        self._pick_color()
        super().mouseReleaseEvent(ev)

    def _pick_color(self):
        if self._alpha_channel:
            color = QColorDialog.getColor(
                self._color, self, options=QColorDialog.ShowAlphaChannel
            )
        else:
            color = QColorDialog.getColor(self._color, self)

        if color.isValid():
            self.set_value(color)

    def _update_ui(self):
        css = "ColorLabel{\n#props\n}"
        props = f"background-color: {self._color.name()};\n"
        if self._display_color_name:
            text_color = get_inverted_color(self._color)
            text_color.setAlpha(255)
            props += f"color: {text_color.name()};"
            display_text = convert_color(self._color, "str", self._alpha_channel)
            self.setText(display_text)

        self.setStyleSheet(css.replace("#props", props))


class ColorDialog(QColorDialog, ValueWidgetMixin):
    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: ColorType,
        *,
        alpha_channel: bool,
    ):
        self._default_value = None
        self._alpha_channel = alpha_channel
        self._accepted = False
        super().__init__(parent)

        self.setWindowModality(Qt.ApplicationModal)
        self.setOption(QColorDialog.ShowAlphaChannel, alpha_channel)

        self.set_value(default_value)

    def accept(self):
        self._accepted = True
        super().accept()

    def reject(self):
        self._accepted = False
        super().reject()

    def get_value(self) -> str:
        cur_color = self.currentColor()
        if self._accepted and cur_color.isValid():
            return convert_color(cur_color, "str", self._alpha_channel)
        return convert_color(self._default_value, "str", self._alpha_channel)

    def set_value(self, value: ColorType):
        self._accepted = False
        self._default_value = to_qcolor(value)
        self.setCurrentColor(self._default_value)


class ColorValue(ValueType):

    def __init__(
        self,
        default_value: ColorType = DEFAULT_VALUE,
        *,
        display_name: Optional[str] = None,
        alpha_channel: bool = ALPHA_CHANNEL,
        display_color_name: bool = DISPLAY_COLOR_NAME,
        widget_height: int = WIDGET_HEIGHT,
        widget_border: bool = WIDGET_BORDER,
    ):

        self.alpha_channel = alpha_channel
        self.display_color_name = display_color_name
        self.min_item_editor_widget_height = widget_height
        self.item_editor_widget_border = widget_border

        default_value = to_qcolor(default_value or DEFAULT_VALUE)
        super().__init__(
            convert_color(default_value, "str", alpha_channel),
            display_name=display_name,
        )

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        return is_valid_color(value)

    def create_item_editor_widget(self, parent: QWidget, *args, **kwargs) -> ColorLabel:
        w = ColorLabel(
            parent,
            default_value=self.default_value,
            alpha_channel=self.alpha_channel,
            display_color_name=self.display_color_name,
            border=self.item_editor_widget_border,
        )
        if self.min_item_editor_widget_height:
            w.setMinimumHeight(self.min_item_editor_widget_height)
        return w

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> ColorDialog:
        return ColorDialog(
            parent, default_value=self.default_value, alpha_channel=self.alpha_channel
        )

    def before_set_editor_data(
        self,
        parent: TableView,
        editor: Union[QWidget, ValueWidgetMixin],
        index: QModelIndex,
    ):
        _ = index  # unused
        if not isinstance(editor, ColorDialog):
            return
        global_pos = parent.mapToGlobal(QPoint(0, 0))
        editor.move(global_pos)

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        if ObjectEditView.is_key_item(col, item):
            return
        bg_color = to_qcolor(value)
        color_name = (
            convert_color(bg_color, "str", self.alpha_channel)
            if self.display_color_name
            else ""
        )
        item.setText(color_name)
        item.setBackground(bg_color)
        item.setForeground(get_inverted_color(bg_color))
        item.setToolTip(color_name)
