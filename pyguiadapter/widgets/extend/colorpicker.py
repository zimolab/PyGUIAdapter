import dataclasses
from typing import Type, Tuple, Union, Literal, Optional

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor, QFont
from qtpy.QtWidgets import QWidget, QLabel, QColorDialog, QFrame

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils

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

        if not isinstance(color, (tuple, QColor, str)):
            raise ValueError("color must be tuple, QColor or str")
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
            text_color = utils.get_inverted_color(self._color)
            text_color.setAlpha(255)
            props += f"color: {text_color.name()};"
            # display_text = self._color.name()
            # if self._alpha_channel:
            #     display_text += f"\nalpha: {self._color.alpha()}"
            display_text = utils.convert_color(self._color, "str", self._alpha_channel)
            self.setText(display_text)

        self.setStyleSheet(css.replace("#props", props))

    @classmethod
    def normalize_color(cls, color: ColorType) -> QColor:
        # if not isinstance(color, (tuple, QColor, str)):
        #     raise ValueError("color must be tuple, QColor or str")
        # if isinstance(color, QColor):
        #     return color
        # if isinstance(color, str):
        #     return QColor(color)
        # if isinstance(color, tuple) and 4 < len(color) < 3:
        #     raise ValueError("color must be tuple of 3 or 4 ints")
        # c = QColor(color[0], color[1], color[2])
        # if len(color) == 4:
        #     c.setAlpha(color[3])
        # return c
        return utils.to_qcolor(color)


@dataclasses.dataclass(frozen=True)
class ColorPickerConfig(CommonParameterWidgetConfig):
    default_value: Optional[ColorType] = "white"
    initial_color: ColorType = "white"
    alpha_channel: bool = True
    display_color_name: bool = True
    min_height: int = 45
    max_height: int = 45
    return_type: Literal["tuple", "QColor", "str"] = "tuple"

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
            self._value_widget.setMinimumHeight(self._config.min_height)
            self._value_widget.setMaximumHeight(self._config.max_height)
        return self._value_widget

    def set_value_to_widget(self, value: ColorType):
        self._value_widget.set_color(value)

    def get_value_from_widget(self) -> ColorType:
        self._config: ColorPickerConfig
        color = self._value_widget.get_color()
        return utils.convert_color(
            color, self._config.return_type, self._config.alpha_channel
        )
        # if self._config.return_type == "tuple":
        #     color_tuple = color.getRgb()
        #     if self._config.alpha_channel:
        #         return color_tuple
        #     return color_tuple[:3]
        # if self._config.return_type == "QColor":
        #     return color
        # return color.name()


@dataclasses.dataclass(frozen=True)
class ColorTuplePickerConfig(ColorPickerConfig):
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
