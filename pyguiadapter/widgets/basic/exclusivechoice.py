import dataclasses
from typing import Type, List, Any, Tuple, Optional, Union

from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QWidget, QGridLayout, QRadioButton, QButtonGroup

from ..common import CommonParameterWidgetConfig, CommonParameterWidget
from ... import utils
from ...fn import ParameterInfo


class _ChoiceButton(QRadioButton):
    def __init__(self, parent: Optional[QWidget], user_data: Any):
        super().__init__(parent)
        self._user_data = user_data

    @property
    def user_data(self) -> Any:
        return self._user_data


# noinspection PyPep8Naming
class _FIRST_OPTION:
    __slots__ = ()


@dataclasses.dataclass(frozen=True)
class ExclusiveChoiceBoxConfig(CommonParameterWidgetConfig):
    default_value: Any = _FIRST_OPTION
    choices: Optional[List[Any]] = None
    columns: int = 1
    show_type_icon: bool = True
    int_icon: utils.IconType = "mdi6.alpha-i-circle"
    bool_icon: str = "mdi6.alpha-b-circle"
    str_icon: str = "mdi6.alpha-s-box"
    object_icon: str_icon = "mdi6.alpha-o-box"
    icon_size: Union[Tuple[int, int], int, QSize, None] = None

    @classmethod
    def target_widget_class(cls) -> Type["ExclusiveChoiceBox"]:
        return ExclusiveChoiceBox


class ExclusiveChoiceBox(CommonParameterWidget):
    ConfigClass = ExclusiveChoiceBoxConfig

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: ExclusiveChoiceBoxConfig,
    ):
        self._value_widget: Optional[QWidget] = None
        self._button_group: Optional[QButtonGroup] = None
        self._button_layout: Optional[QGridLayout] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QWidget:
        self._config: ExclusiveChoiceBoxConfig
        if self._value_widget is None:
            self._value_widget = QWidget(self)
            self._button_layout = QGridLayout()
            self._value_widget.setLayout(self._button_layout)
            self._button_group = QButtonGroup(self._value_widget)
            self._button_group.setExclusive(True)
            self._add_choices()
        return self._value_widget

    def set_value_to_widget(self, value: Any):
        if value is _FIRST_OPTION:
            self._button_group.buttons()[0].setChecked(True)
            return
        for btn in self._button_group.buttons():
            assert isinstance(btn, _ChoiceButton)
            user_data = btn.user_data
            if user_data == value:
                btn.setChecked(True)
                break

    def get_value_from_widget(self) -> Any:
        for btn in self._button_group.buttons():
            assert isinstance(btn, _ChoiceButton)
            if btn.isChecked():
                return btn.user_data
        return None

    def _add_choices(self):
        self._config: ExclusiveChoiceBoxConfig
        choices = utils.unique_list(self._config.choices)
        cols = max(self._config.columns, 1)
        for idx, choice in enumerate(choices):
            btn = _ChoiceButton(self._value_widget, choice)
            icon_size = utils.get_size(self._config.icon_size)
            if icon_size is not None:
                btn.setIconSize(icon_size)
            btn.setText(str(choice))
            if self._config.show_type_icon:
                str_icon = utils.get_icon(self._config.str_icon) or QIcon()
                bool_icon = utils.get_icon(self._config.bool_icon) or QIcon()
                int_icon = utils.get_icon(self._config.int_icon) or QIcon()
                object_icon = utils.get_icon(self._config.object_icon) or QIcon()
                if isinstance(choice, str):
                    btn.setIcon(str_icon)
                elif isinstance(choice, bool):
                    btn.setIcon(bool_icon)
                elif isinstance(choice, int):
                    btn.setIcon(int_icon)
                else:
                    btn.setIcon(object_icon)
            self._button_group.addButton(btn)
            if idx % cols == 0:
                self._button_layout.addWidget(btn, idx // cols, 0)
            else:
                self._button_layout.addWidget(btn, idx // cols, idx % cols)

    @classmethod
    def on_post_process_config(
        cls,
        config: ExclusiveChoiceBoxConfig,
        parameter_name: str,
        parameter_info: ParameterInfo,
    ) -> ExclusiveChoiceBoxConfig:
        if not config.choices and len(parameter_info.type_args) > 0:
            config = dataclasses.replace(
                config, choices=parameter_info.type_args.copy()
            )
        return config
