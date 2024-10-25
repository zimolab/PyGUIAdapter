import dataclasses
from typing import Type, List, Any, Dict, Optional, Union

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QComboBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


# noinspection PyPep8Naming
class _FIRST_ITEM(object):
    __slots__ = ()


@dataclasses.dataclass
class _DataWrap(object):
    value: Any


@dataclasses.dataclass(frozen=True)
class ChoiceBoxConfig(CommonParameterWidgetConfig):
    """ChoiceBox的配置类"""

    default_value: Optional[Any] = _FIRST_ITEM
    """默认选项，`_FIRST_ITEM`是一个特殊值，表示选择选项列表中的第一个"""

    choices: Union[Dict[str, Any], List[Any]] = dataclasses.field(default_factory=list)
    """选项列表，可以是字典或列表。为字典时，键值对的键为显示文本，值为实际值；为列表时，对每个元素调用`str()`，以其返回值作为显示文本，元素本身作为实际值。"""

    editable: bool = False
    """是否允许编辑"""

    @classmethod
    def target_widget_class(cls) -> Type["ChoiceBox"]:
        return ChoiceBox


class ChoiceBox(CommonParameterWidget):
    ConfigClass = ChoiceBoxConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: ChoiceBoxConfig,
    ):
        self._value_widget: Optional[QComboBox] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: ChoiceBoxConfig
        if self._value_widget is None:
            self._value_widget = QComboBox(self)
            if self._config.editable:
                self._value_widget.setEditable(True)
            self._add_choices()
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        if value is _FIRST_ITEM:
            self._value_widget.setCurrentIndex(0)
            return
        for index in range(self._value_widget.count()):
            data = self._value_widget.itemData(index, Qt.UserRole)
            if isinstance(data, _DataWrap):
                data = data.value
            if data == value:
                self._value_widget.setCurrentIndex(index)
                break

    def get_value_from_widget(self) -> Any:
        data = self._value_widget.currentData(Qt.UserRole)
        if isinstance(data, _DataWrap):
            return data.value
        if data is not None:
            return data
        return self._value_widget.currentText()

    def _add_choices(self):
        self._config: ChoiceBoxConfig
        choices = self._config.choices
        assert isinstance(choices, list) or isinstance(choices, dict)
        if isinstance(choices, list):
            for choice in choices:
                self._value_widget.addItem(str(choice), _DataWrap(choice))
            return

        if isinstance(choices, dict):
            for key, value in choices.items():
                self._value_widget.addItem(key, _DataWrap(value))
            return
