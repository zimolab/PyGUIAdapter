from typing import Optional, Any, Union, Tuple

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QFont
from qtpy.QtWidgets import QWidget, QLabel, QFrame, QColorDialog, QVBoxLayout

from ..schema import CellWidgetMixin, ValueType
from ...ui_utilities import is_valid_color, to_qcolor, get_inverted_color, convert_color

DEFAULT_VALUE = "#FFFFFF"
ALPHA_CHANNEL = False
DISPLAY_COLOR_NAME = True
RETURN_COLOR_TYPE = "str"
BORDER = False
EDIT_ON_DOUBLE_CLICK = False
CELL_WIDGET_MARGINS = (10, 10, 10, 10)
MIN_ITEM_EDITOR_WIDGET_HEIGHT = 50


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
        edit_on_double_click: bool = EDIT_ON_DOUBLE_CLICK,
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
        self._edit_on_double_click = edit_on_double_click

        self.set_value(default_value)

    def set_value(self, color: ColorType):
        self._color = self.normalize_color(color)
        self._update_ui()

    def get_value(self) -> Union[str, Tuple[int, int, int, int], QColor]:
        # noinspection PyTypeChecker
        return convert_color(self._color, self._return_color_type, self._alpha_channel)

    def mouseReleaseEvent(self, ev):
        if not self._edit_on_double_click:
            self._pick_color()
        super().mouseReleaseEvent(ev)

    def mouseDoubleClickEvent(self, event):
        if self._edit_on_double_click:
            self._pick_color()
        super().mouseDoubleClickEvent(event)

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


class ColorWidget(QWidget, CellWidgetMixin):
    def __init__(
        self,
        parent: Optional[QWidget],
        default_value: ColorType = DEFAULT_VALUE,
        *,
        alpha_channel: bool = ALPHA_CHANNEL,
        display_color_name: bool = DISPLAY_COLOR_NAME,
        return_color_type: str = RETURN_COLOR_TYPE,
        border: bool = BORDER,
        edit_on_double_click: bool = EDIT_ON_DOUBLE_CLICK,
        cell_widget_margins: Tuple[int, int, int, int] = CELL_WIDGET_MARGINS,
    ):
        super().__init__(parent)
        self._layout = QVBoxLayout()
        if cell_widget_margins:
            self._layout.setContentsMargins(*cell_widget_margins)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self._color_label = ColorLabel(
            self,
            default_value=default_value,
            alpha_channel=alpha_channel,
            display_color_name=display_color_name,
            return_color_type=return_color_type,
            border=border,
            edit_on_double_click=edit_on_double_click,
        )
        self._layout.addWidget(self._color_label)

    def set_value(self, value: ColorType):
        self._color_label.set_value(value)

    def get_value(self) -> Union[str, Tuple[int, int, int, int], QColor]:
        return self._color_label.get_value()


class ColorValue(ValueType):

    def __init__(
        self,
        default_value: ColorType = DEFAULT_VALUE,
        *,
        alpha_channel: bool = ALPHA_CHANNEL,
        display_color_name: bool = DISPLAY_COLOR_NAME,
        return_color_type: str = RETURN_COLOR_TYPE,
        border: bool = BORDER,
        edit_on_double_click: bool = EDIT_ON_DOUBLE_CLICK,
        cell_widget_margins: Tuple[int, int, int, int] = CELL_WIDGET_MARGINS,
        min_item_editor_widget_height: int = MIN_ITEM_EDITOR_WIDGET_HEIGHT,
    ):
        if default_value is None:
            default_value = DEFAULT_VALUE

        if not return_color_type in ("str", "tuple", "QColor"):
            raise ValueError(f"invalid return_color_type: {return_color_type}")

        super().__init__(to_qcolor(default_value))

        self.alpha_channel = alpha_channel
        self.display_color_name = display_color_name
        self.return_color_type = return_color_type
        self.border = border
        self.edit_on_double_click = edit_on_double_click
        self.cell_widget_margins = cell_widget_margins
        self.min_item_editor_widget_height = min_item_editor_widget_height

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        return is_valid_color(value)

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> ColorWidget:
        w = ColorLabel(
            parent,
            default_value=self.default_value,
            alpha_channel=self.alpha_channel,
            display_color_name=self.display_color_name,
            return_color_type=self.return_color_type,
            border=self.border,
            edit_on_double_click=self.edit_on_double_click,
        )
        if self.min_item_editor_widget_height:
            w.setMinimumHeight(self.min_item_editor_widget_height)
        return w

    def create_item_delegate_widget(self, parent: QWidget, *args, **kwargs) -> None:
        return None

    def create_cell_widget(
        self, parent: QWidget, row: int, col: int, *args, **kwargs
    ) -> ColorLabel:
        return ColorWidget(
            parent,
            default_value=self.default_value,
            alpha_channel=self.alpha_channel,
            display_color_name=self.display_color_name,
            return_color_type=self.return_color_type,
            border=self.border,
            edit_on_double_click=self.edit_on_double_click,
            cell_widget_margins=self.cell_widget_margins,
        )
