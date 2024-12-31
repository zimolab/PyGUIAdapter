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
from .._commons import KEY_COLUMN_INDEX
from ..schema import ValueType, ValueWidgetMixin
from ...tableview import TableView
from ...ui_utilities import is_valid_color, to_qcolor, get_inverted_color, convert_color

DEFAULT_VALUE = "#FFFFFF"
ALPHA_CHANNEL = False
DISPLAY_COLOR_NAME = True
RETURN_COLOR_TYPE = "str"
BORDER = False
EDIT_ON_DOUBLE_CLICK = False
CELL_WIDGET_MARGINS = (10, 10, 10, 10)
MIN_ITEM_EDITOR_WIDGET_HEIGHT = 35


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
        default_value: ColorType = DEFAULT_VALUE,
        *,
        alpha_channel: bool = ALPHA_CHANNEL,
        display_color_name: bool = DISPLAY_COLOR_NAME,
        return_color_type: str = RETURN_COLOR_TYPE,
        border: bool = BORDER,
    ):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        if border:
            self.setFrameShape(QFrame.Box)
            self.setFrameShadow(QFrame.Raised)

        font: QFont = self.font()
        font.setBold(True)
        self.setFont(font)

        self._color = default_value
        self._alpha_channel = alpha_channel
        self._display_color_name = display_color_name
        self._return_color_type = return_color_type

        self.set_value(default_value)

    def set_value(self, color: ColorType):
        self._color = self.normalize_color(color)
        self._update_ui()

    def get_value(self) -> Union[str, Tuple[int, int, int, int], QColor]:
        # noinspection PyTypeChecker
        return convert_color(self._color, self._return_color_type, self._alpha_channel)

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

    @classmethod
    def normalize_color(cls, color: ColorType) -> QColor:
        return to_qcolor(color)


class ColorDialog(QColorDialog, ValueWidgetMixin):
    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: ColorType = DEFAULT_VALUE,
        *,
        alpha_channel: bool = ALPHA_CHANNEL,
        return_color_type: str = RETURN_COLOR_TYPE,
    ):
        self._default_value = to_qcolor(default_value)
        self._return_color_type = return_color_type
        self._alpha_channel = alpha_channel
        self._accepted = False

        super().__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setOption(QColorDialog.ShowAlphaChannel, alpha_channel)
        self.set_value(default_value)

    def accept(self):
        self._accepted = True
        super().accept()

    def get_value(self) -> ColorType:
        cur_color = self.currentColor()
        if not self._accepted or not cur_color.isValid():
            # noinspection PyTypeChecker
            return convert_color(
                self._default_value, self._return_color_type, self._alpha_channel
            )
        # noinspection PyTypeChecker
        return convert_color(cur_color, self._return_color_type, self._alpha_channel)

    def set_value(self, value: ColorType):
        self._accepted = False
        self._default_value = to_qcolor(value)
        self.setCurrentColor(self._default_value)


class ColorValue(ValueType):

    def __init__(
        self,
        default_value: ColorType = DEFAULT_VALUE,
        *,
        alpha_channel: bool = ALPHA_CHANNEL,
        display_color_name: bool = DISPLAY_COLOR_NAME,
        return_color_type: str = RETURN_COLOR_TYPE,
        cell_widget_margins: Tuple[int, int, int, int] = CELL_WIDGET_MARGINS,
        min_item_editor_widget_height: int = MIN_ITEM_EDITOR_WIDGET_HEIGHT,
        item_editor_widget_border: bool = BORDER,
    ):
        if default_value is None:
            default_value = DEFAULT_VALUE

        if not return_color_type in ("str", "tuple", "QColor"):
            raise ValueError(f"invalid return_color_type: {return_color_type}")

        super().__init__(convert_color(to_qcolor(default_value), "str", alpha_channel))

        self.alpha_channel = alpha_channel
        self.display_color_name = display_color_name
        self.return_color_type = return_color_type
        self.cell_widget_margins = cell_widget_margins
        self.min_item_editor_widget_height = min_item_editor_widget_height
        self.item_editor_widget_border = item_editor_widget_border

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
            return_color_type=self.return_color_type,
            border=self.item_editor_widget_border,
        )
        if self.min_item_editor_widget_height:
            w.setMinimumHeight(self.min_item_editor_widget_height)
        return w

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> ColorDialog:
        return ColorDialog(
            parent,
            default_value=self.default_value,
            alpha_channel=self.alpha_channel,
            return_color_type=self.return_color_type,
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
        if not item:
            return
        if isinstance(item.tableWidget(), ObjectEditView) and col == KEY_COLUMN_INDEX:
            return
        bg_color = to_qcolor(value)
        text = convert_color(bg_color, "str", self.alpha_channel)
        if self.display_color_name:
            item.setText(text)
        else:
            item.setText("")
        item.setBackground(bg_color)
        item.setForeground(get_inverted_color(bg_color))
        item.setToolTip(text)
