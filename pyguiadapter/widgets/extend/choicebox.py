import dataclasses
from typing import Type, Any, Dict, Optional, Union, Sequence

from qtpy.QtCore import Qt
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QWidget, QComboBox

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


# noinspection PyPep8Naming
class _FIRST_ITEM(object):
    __slots__ = ()


@dataclasses.dataclass
class _DataWrap(object):
    value: Any

    @classmethod
    def unwrap(cls, data: Any) -> Any:
        if isinstance(data, cls):
            return data.value
        return data


class _ChoiceComboBox(QComboBox):
    def __init__(self, parent: Optional[QWidget] = None, add_user_input: bool = True):
        super().__init__(parent)
        self._add_user_input = add_user_input

    @property
    def add_user_input(self) -> bool:
        return self._add_user_input

    @add_user_input.setter
    def add_user_input(self, value: bool):
        self._add_user_input = value

    def keyPressEvent(self, e: QKeyEvent):
        if self._add_user_input:
            super().keyPressEvent(e)
            return
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            e.ignore()
            return
        super().keyPressEvent(e)


@dataclasses.dataclass(frozen=True)
class ChoiceBoxConfig(CommonParameterWidgetConfig):
    """ChoiceBox的配置类"""

    default_value: Optional[Any] = _FIRST_ITEM
    """默认选项，`_FIRST_ITEM`是一个特殊值，表示选择选项列表中的第一个"""

    choices: Union[Dict[str, Any], Sequence[Any]] = dataclasses.field(
        default_factory=list
    )
    """选项列表，可以是字典或列表、元组等序列对象。为字典时，键值对的键为显示文本，值为实际值；为序列对象时，对序列中的每个元素调用`str()`，
    以其返回值作为显示文本，元素本身作为实际值。"""

    editable: bool = False
    """是否允许编辑"""

    add_user_input: bool = True
    """在`editable`为`True`时，用户输入的内容是否作为新的选项添加到选项列表中"""

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
        self._value_widget: Optional[_ChoiceComboBox] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: ChoiceBoxConfig
        if self._value_widget is None:
            self._value_widget = _ChoiceComboBox(self, self._config.add_user_input)
            self._value_widget.setEditable(self._config.editable is True)
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
        if self._value_widget.isEditable():
            # For an editable ChoiceBox, if the currentText() is not consistent with itemText(currentIndex()), it means
            # the user has input a new text, in this case, we should return the new input text, otherwise we should
            # return the currentData().
            current_text = self._value_widget.currentText()
            item_text = self._value_widget.itemText(self._value_widget.currentIndex())
            if current_text != item_text:
                return current_text
            data = _DataWrap.unwrap(self._value_widget.currentData(Qt.UserRole))
            if data is not None:
                return data
            else:
                return current_text

        data = _DataWrap.unwrap(self._value_widget.currentData(Qt.UserRole))
        if data is not None:
            return data
        else:
            return self._value_widget.currentText()

    def _add_choices(self):
        self._config: ChoiceBoxConfig
        choices = self._config.choices
        if isinstance(choices, dict):
            for key, value in choices.items():
                self._value_widget.addItem(key, _DataWrap(value))
            return

        if isinstance(choices, (list, tuple, set)):
            for choice in choices:
                self._value_widget.addItem(str(choice), _DataWrap(choice))
            return
