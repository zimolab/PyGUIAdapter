import dataclasses

from qtpy.QtWidgets import QWidget, QButtonGroup, QRadioButton, QVBoxLayout, QHBoxLayout
from typing import Type, Optional, Any

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ...utils import IconType, get_icon, type_check


@dataclasses.dataclass(frozen=True)
class BoolBoxConfig(CommonParameterWidgetConfig):
    default_value: Optional[bool] = False
    true_text: str = "True"
    false_text: str = "False"
    true_icon: IconType = None
    false_icon: IconType = None
    vertical: bool = False

    @classmethod
    def target_widget_class(cls) -> Type["BoolBox"]:
        return BoolBox


class BoolBox(CommonParameterWidget):
    ConfigClass: Type[BoolBoxConfig] = BoolBoxConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: BoolBoxConfig,
    ):
        self._value_widget: Optional[QWidget] = None
        self._true_radio_button: Optional[QRadioButton] = None
        self._false_radio_button: Optional[QRadioButton] = None
        self._button_group: Optional[QButtonGroup] = None

        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        if self._value_widget is None:
            config: BoolBoxConfig = self.config

            self._value_widget = QWidget(self)
            if config.vertical:
                layout = QVBoxLayout()
            else:
                layout = QHBoxLayout()
            self._value_widget.setLayout(layout)

            self._true_radio_button = QRadioButton(self._value_widget)
            self._true_radio_button.setText(config.true_text)
            true_icon = get_icon(config.true_icon)
            if true_icon is not None:
                self._true_radio_button.setIcon(true_icon)

            self._false_radio_button = QRadioButton(self._value_widget)
            self._false_radio_button.setText(config.false_text)
            false_icon = get_icon(config.false_icon)
            if false_icon is not None:
                self._false_radio_button.setIcon(false_icon)

            self._button_group = QButtonGroup(self._value_widget)
            self._button_group.addButton(self._true_radio_button)
            self._button_group.addButton(self._false_radio_button)
            self._button_group.setExclusive(True)

            layout.addWidget(self._true_radio_button)
            layout.addWidget(self._false_radio_button)

        return self._value_widget

    def check_value_type(self, value: Any):
        type_check(value, (bool, int), allow_none=True)

    def set_value_to_widget(self, value: bool):
        if value:
            self._true_radio_button.setChecked(True)
        else:
            self._false_radio_button.setChecked(True)

    def get_value_from_widget(self) -> bool:
        return self._true_radio_button.isChecked()
