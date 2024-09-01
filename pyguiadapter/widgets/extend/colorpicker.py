from __future__ import annotations

import dataclasses
from typing import Type, TypeVar, Tuple, Union, Literal

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
]


class ColorLabel(QLabel):
    def __init__(
        self,
        parent: QWidget | None,
        show_alpha: bool = True,
        initial_color: ColorType = Qt.white,
        show_color_name: bool = True,
    ):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)

        font: QFont = self.font()
        font.setBold(True)
        self.setFont(font)

        self._color = initial_color
        self._show_alpha = show_alpha
        self._show_color_name = show_color_name

        self.set_color(initial_color)

    def set_color(self, color: ColorType):
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
        if self._show_alpha:
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
        if self._show_color_name:
            text_color = utils.get_inverted_color(self._color)
            text_color.setAlpha(255)
            props += f"color: {text_color.name()};"
        self.setStyleSheet(css.replace("#props", props))
        self.setText(self._color.name())

    @classmethod
    def normalize_color(cls, color: ColorType) -> QColor:
        if not isinstance(color, (tuple, QColor, str)):
            raise ValueError("color must be tuple, QColor or str")
        if isinstance(color, QColor):
            return color
        if isinstance(color, str):
            return QColor(color)
        if isinstance(color, tuple) and 4 < len(color) < 3:
            raise ValueError("color must be tuple of 3 or 4 ints")
        c = QColor(color[0], color[1], color[2])
        if len(color) == 4:
            c.setAlpha(color[3])
        return c


@dataclasses.dataclass(frozen=True)
class ColorPickerConfig(CommonParameterWidgetConfig):
    default_value: ColorType | None = None
    initial_color: ColorType = "white"
    show_alpha: bool = True
    show_color_name: bool = True
    min_height: int = 45
    max_height: int = 45
    return_type: Literal["tuple", "QColor", "str"] = "tuple"

    @classmethod
    def target_widget_class(cls) -> Type["ColorPicker"]:
        return ColorPicker


class ColorPicker(CommonParameterWidget):
    Self = TypeVar("Self", bound="ColorPicker")
    ConfigClass = ColorPickerConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: ColorPickerConfig,
    ):
        self._config: ColorPickerConfig = config
        self._value_widget: ColorLabel | None = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLabel:
        if self._value_widget is None:
            self._value_widget = ColorLabel(
                self,
                self._config.show_alpha,
                self._config.initial_color,
                self._config.show_color_name,
            )
            self._value_widget.setMinimumHeight(self._config.min_height)
            self._value_widget.setMaximumHeight(self._config.max_height)
        return self._value_widget

    def set_value_to_widget(self, value: ColorType):
        self._value_widget.set_color(value)

    def get_value_from_widget(self) -> ColorType:
        color = self._value_widget.get_color()
        if self._config.return_type == "tuple":
            color_tuple = color.getRgb()
            if self._config.show_alpha:
                return color_tuple
            return color_tuple[:3]
        if self._config.return_type == "QColor":
            return color
        return color.name()


class ColorTuplePicker(ColorPicker):
    Self = TypeVar("Self", bound="ColorTuplePicker")
    ConfigClass = ColorPickerConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: ColorPickerConfig,
    ):
        config = dataclasses.replace(config, return_type="tuple")
        super().__init__(parent, parameter_name, config)


class ColorHexPicker(ColorPicker):
    Self = TypeVar("Self", bound="ColorHexPicker")
    ConfigClass = ColorPickerConfig

    def __init__(
        self,
        parent: QWidget | None,
        parameter_name: str,
        config: ColorPickerConfig,
    ):
        config = dataclasses.replace(config, return_type="str")
        super().__init__(parent, parameter_name, config)
