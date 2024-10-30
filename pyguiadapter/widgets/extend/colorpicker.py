import dataclasses

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QFont
from qtpy.QtWidgets import QWidget, QLabel, QColorDialog, QFrame
from typing import Type, Tuple, Union, Literal, Optional, Any

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import to_qcolor, get_inverted_color, convert_color, type_check

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
        alpha_channel: bool = True,
        initial_color: ColorType = Qt.white,
        display_color_name: bool = True,
    ):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)

        font: QFont = self.font()
        font.setBold(True)
        self.setFont(font)

        self._color = initial_color
        self._alpha_channel = alpha_channel
        self._display_color_name = display_color_name

        self.set_color(initial_color)

    def set_color(self, color: ColorType):
        if isinstance(color, list):
            color = tuple(color)

        if isinstance(color, tuple):
            if len(color) not in (3, 4):
                raise ValueError("color tuple or list must have 3 or 4 elements")

        if not isinstance(color, (tuple, QColor, str)):
            raise ValueError(f"invalid color type: {type(color)}")
        self._color = self.normalize_color(color)
        self._update_ui()

    def get_color(self) -> QColor:
        return self._color

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
            self.set_color(color)

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


@dataclasses.dataclass(frozen=True)
class ColorPickerConfig(CommonParameterWidgetConfig):
    """ColorPicker的配置类"""

    default_value: Optional[ColorType] = "white"
    """默认颜色值，可以为颜色名称，RGB（或RGBA）字符串，QColor，或颜色元组（列表）"""

    initial_color: ColorType = "white"

    alpha_channel: bool = True
    """是否显示Alpha通道"""

    display_color_name: bool = True
    """颜色标签上是否显示颜色名称"""

    width: Optional[int] = None
    """颜色标签的宽度"""

    height: Optional[int] = 45
    """颜色标签的高度"""

    return_type: Literal["tuple", "QColor", "str"] = "tuple"
    """返回值类型，即从控件获取值时得到的值的类型，可以为“tuple”（返回RGB或RGBA元组），“QColor”（返回QColor对象），
    或“str”（返回RGB或RGBA十六进制字符串）"""

    @classmethod
    def target_widget_class(cls) -> Type["ColorPicker"]:
        return ColorPicker


class ColorPicker(CommonParameterWidget):
    ConfigClass = ColorPickerConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: ColorPickerConfig,
    ):
        self._value_widget: Optional[ColorLabel] = None
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        if isinstance(value, (list, tuple)):
            if len(value) in (3, 4):
                return
            else:
                raise ValueError("color tuple or list must have 3 or 4 elements")
        type_check(value, (QColor, str), allow_none=True)

    @property
    def value_widget(self) -> QLabel:
        self._config: ColorPickerConfig
        if self._value_widget is None:
            self._value_widget = ColorLabel(
                self,
                self._config.alpha_channel,
                self._config.initial_color,
                self._config.display_color_name,
            )
            if self._config.width is not None:
                self._value_widget.setFixedWidth(self._config.width)
            if self._config.height is not None:
                self._value_widget.setFixedHeight(self._config.height)
        return self._value_widget

    def set_value_to_widget(self, value: ColorType):
        self._value_widget.set_color(value)

    def get_value_from_widget(self) -> ColorType:
        self._config: ColorPickerConfig
        color = self._value_widget.get_color()
        return convert_color(
            color, self._config.return_type, self._config.alpha_channel
        )


@dataclasses.dataclass(frozen=True)
class ColorTuplePickerConfig(ColorPickerConfig):
    """ColorTuplePicker的配置类"""

    return_type = "tuple"

    @classmethod
    def target_widget_class(cls) -> Type["ColorTuplePicker"]:
        return ColorTuplePicker


class ColorTuplePicker(ColorPicker):
    ConfigClass = ColorTuplePickerConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: ColorPickerConfig,
    ):
        config = dataclasses.replace(config, return_type="tuple")
        super().__init__(parent, parameter_name, config)


@dataclasses.dataclass(frozen=True)
class ColorHexPickerConfig(ColorPickerConfig):
    """ColorHexPicker的配置类"""

    return_type = "str"

    @classmethod
    def target_widget_class(cls) -> Type["ColorHexPicker"]:
        return ColorHexPicker


class ColorHexPicker(ColorPicker):
    ConfigClass = ColorHexPickerConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: ColorPickerConfig,
    ):
        config = dataclasses.replace(config, return_type="str")
        super().__init__(parent, parameter_name, config)
