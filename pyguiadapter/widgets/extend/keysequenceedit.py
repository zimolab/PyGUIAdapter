import dataclasses
from typing import Type, Union, Optional, Any, Literal, List

from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import QWidget, QKeySequenceEdit

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import type_check

KeySequenceFormat = QKeySequence.SequenceFormat


@dataclasses.dataclass(frozen=True)
class KeySequenceEditConfig(CommonParameterWidgetConfig):
    """KeySequenceEdit的配置类。"""

    default_value: Union[str, QKeySequence, None] = ""
    """控件的默认值"""

    key_sequence_format: KeySequenceFormat = QKeySequence.PortableText
    """按键序列格式"""

    return_type: Literal["str", "list"] = "str"
    """返回值类型"""

    @classmethod
    def target_widget_class(cls) -> Type["KeySequenceEdit"]:
        return KeySequenceEdit


class KeySequenceEdit(CommonParameterWidget):
    ConfigClass = KeySequenceEditConfig

    PortableText = QKeySequence.PortableText
    """按键序列格式：PortableText"""

    NativeText = QKeySequence.NativeText
    """按键序列格式：NativeText"""

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

    def get_value_from_widget(self) -> Union[str, List[str]]:
        self._config: KeySequenceEditConfig
        key_sequence = self._value_widget.keySequence()
        if self._config.return_type == "str":
            return key_sequence.toString(self._config.key_sequence_format)
        else:
            return self.split_key_sequences(
                key_sequence.toString(self._config.key_sequence_format)
            )

    @staticmethod
    def split_key_sequences(key_sequences: str) -> list:
        """
        将一组按键序列字符串分割成单个按键序列组成的列表。

        比如：

        "Ctrl+Alt+A, Ctrl+B, Ctrl+C" -> ["Ctrl+Alt+A", "Ctrl+B", "Ctrl+C"]

        又比如：

        "Ctrl+A, Ctrl+B, ,, Ctrl+,, B, C" -> ["Ctrl+A", "Ctrl+B", "Ctrl+,", ",", "B", "C"]

        Args:
            key_sequences: 按键序列字符串

        Returns:
            按键序列组成的列表
        """
        return [seq.strip() for seq in key_sequences.split(", ") if seq.strip() != ""]
