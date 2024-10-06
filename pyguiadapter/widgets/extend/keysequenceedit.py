import dataclasses
from typing import Type, Union, Optional, Any

from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import QWidget, QKeySequenceEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check

KeySequenceFormat = QKeySequence.SequenceFormat


@dataclasses.dataclass(frozen=True)
class KeySequenceEditConfig(CommonParameterWidgetConfig):
    default_value: Union[str, QKeySequence, None] = ""
    key_sequence_format: KeySequenceFormat = QKeySequence.PortableText

    @classmethod
    def target_widget_class(cls) -> Type["KeySequenceEdit"]:
        return KeySequenceEdit


class KeySequenceEdit(CommonParameterWidget):
    ConfigClass = KeySequenceEditConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: KeySequenceEditConfig,
    ):
        self._value_widget: Optional[QKeySequenceEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QKeySequenceEdit:
        if self._value_widget is None:
            self._value_widget = QKeySequenceEdit(self)
        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (str, QKeySequence), allow_none=True)

    def set_value_to_widget(self, value: Union[str, QKeySequence]):
        self._config: KeySequenceEditConfig
        if isinstance(value, str):
            value = QKeySequence(value, self._config.key_sequence_format)
        self._value_widget.setKeySequence(value)

    def get_value_from_widget(self) -> str:
        self._config: KeySequenceEditConfig
        key_sequence = self._value_widget.keySequence()
        return key_sequence.toString(self._config.key_sequence_format)
