import dataclasses
from typing import Type, List, Any, Dict, Optional, Union, Sequence

from qtpy.QtWidgets import QWidget, QGridLayout, QCheckBox, QButtonGroup

from ..common import CommonParameterWidgetConfig, CommonParameterWidget


class _CheckBox(QCheckBox):
    def __init__(self, parent: Optional[QWidget], user_data: Any):
        super().__init__(parent)
        self._user_data = user_data

    @property
    def user_data(self) -> Any:
        return self._user_data


@dataclasses.dataclass(frozen=True)
class MultiChoiceBoxConfig(CommonParameterWidgetConfig):
    """MultiChoiceBox的配置类。"""

    default_value: Optional[Sequence[Any]] = dataclasses.field(default_factory=list)
    """默认选中的值"""

    choices: Union[Sequence[Any], Dict[str, Any]] = dataclasses.field(
        default_factory=list
    )
    """可选项列表。为字典时，将键值对的键作为显示文本，键值对的值作为实际的值；否则，对每个选项调用str()，将返回值作为显示文本，选项本身作为实际的值。"""

    columns: int = 1
    """选项的列数"""

    @classmethod
    def target_widget_class(cls) -> Type["MultiChoiceBox"]:
        return MultiChoiceBox


class MultiChoiceBox(CommonParameterWidget):
    ConfigClass = MultiChoiceBoxConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: MultiChoiceBoxConfig,
    ):
        self._value_widget: Optional[QWidget] = None
        self._button_layout: Optional[QGridLayout] = None
        self._button_group: Optional[QButtonGroup] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._button_layout = QGridLayout()
            self._button_group = QButtonGroup(self._value_widget)
            self._button_group.setExclusive(False)
            self._value_widget.setLayout(self._button_layout)
            self._add_choices()

        return self._value_widget

    def set_value_to_widget(self, value: Sequence[Any]):
        if not isinstance(value, (list, set, tuple)):
            value = [value]
        for btn in self._button_group.buttons():
            if btn.user_data in value:
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def get_value_from_widget(self) -> List[Any]:
        ret = []
        for btn in self._button_group.buttons():
            if btn.isChecked():
                ret.append(btn.user_data)
        return ret

    def _add_choices(self):
        self._config: MultiChoiceBoxConfig
        assert isinstance(self._config.choices, (list, tuple, set, dict))
        cols = max(self._config.columns, 1)
        if isinstance(self._config.choices, (list, tuple, set)):
            for idx, choice in enumerate(self._config.choices):
                button = _CheckBox(self, choice)
                button.setText(str(choice))
                self._button_group.addButton(button)
                if idx % cols == 0:
                    self._button_layout.addWidget(button, idx // cols, 0)
                else:
                    self._button_layout.addWidget(button, idx // cols, idx % cols)
            return

        if isinstance(self._config.choices, dict):
            for idx, (key, value) in enumerate(self._config.choices.items()):
                button = _CheckBox(self, value)
                button.setText(key)
                self._button_group.addButton(button)
                if idx % cols == 0:
                    self._button_layout.addWidget(button, idx // cols, 0)
                else:
                    self._button_layout.addWidget(button, idx // cols, idx % cols)
