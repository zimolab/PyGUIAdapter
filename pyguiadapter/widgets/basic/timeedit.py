import dataclasses
from datetime import time, datetime
from typing import Type, Union, Optional, Any

from qtpy.QtCore import Qt, QTime
from qtpy.QtWidgets import QWidget, QTimeEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check

Alignment = Qt.AlignmentFlag
ButtonSymbols = QTimeEdit.ButtonSymbols
CorrectionMode = QTimeEdit.CorrectionMode
TimeSpec = Qt.TimeSpec


@dataclasses.dataclass(frozen=True)
class TimeEditConfig(CommonParameterWidgetConfig):
    default_value: Union[time, QTime, None] = datetime.now().time()
    min_time: Union[time, QTime, None] = None
    max_time: Union[time, QTime, None] = None
    display_format: Optional[str] = None
    time_spec: Optional[TimeSpec] = None
    wrapping: bool = False
    frame: bool = True
    alignment: Alignment = Qt.AlignLeft | Qt.AlignVCenter
    button_symbols: Optional[ButtonSymbols] = None
    correction_mode: Optional[CorrectionMode] = None
    keyboard_tracking: bool = True
    accelerated: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["TimeEdit"]:
        return TimeEdit


class TimeEdit(CommonParameterWidget):
    ConfigClass = TimeEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: TimeEditConfig,
    ):
        self._value_widget: Optional[QTimeEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: TimeEditConfig
        if self._value_widget is None:
            self._value_widget = QTimeEdit(self)
            if self._config.min_time is not None:
                self._value_widget.setMinimumTime(QTime(self._config.min_time))

            if self._config.max_time is not None:
                self._value_widget.setMaximumTime(QTime(self._config.max_time))

            if self._config.display_format is not None:
                self._value_widget.setDisplayFormat(self._config.display_format)

            if self._config.time_spec is not None:
                self._value_widget.setTimeSpec(self._config.time_spec)

            self._value_widget.setWrapping(self._config.wrapping)
            self._value_widget.setFrame(self._config.frame)
            self._value_widget.setAlignment(self._config.alignment)
            if self._config.button_symbols is not None:
                self._value_widget.setButtonSymbols(self._config.button_symbols)
            if self._config.correction_mode is not None:
                self._value_widget.setCorrectionMode(self._config.correction_mode)
            self._value_widget.setKeyboardTracking(self._config.keyboard_tracking)
            self._value_widget.setAccelerated(self._config.accelerated)

        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, allowed_types=(time, QTime), allow_none=True)

    def set_value_to_widget(self, value: Union[time, QTime]):
        if isinstance(value, QTime):
            pass
        elif isinstance(value, time):
            value = QTime(value)
        else:
            raise TypeError(f"invalid type: {type(value)}")
        self._value_widget.setTime(value)

    def get_value_from_widget(self) -> time:
        value = self._value_widget.time()
        return value.toPython()
