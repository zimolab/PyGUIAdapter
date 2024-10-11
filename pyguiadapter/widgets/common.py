import copy
import dataclasses
from abc import abstractmethod
from typing import Any, Type, Optional

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QCheckBox,
    QSpacerItem,
    QSizePolicy,
)

from ..exceptions import ParameterError
from ..paramwidget import BaseParameterWidgetConfig, BaseParameterWidget


@dataclasses.dataclass(frozen=True)
class CommonParameterWidgetConfig(BaseParameterWidgetConfig):

    set_default_value_on_init: bool = True
    hide_default_value_checkbox: bool = True
    set_deepcopy: bool = True
    get_deepcopy: bool = True

    @classmethod
    def target_widget_class(cls) -> Type["CommonParameterWidget"]:
        return CommonParameterWidget


class CommonParameterWidget(BaseParameterWidget):
    ConfigClass: Type[CommonParameterWidgetConfig] = NotImplemented

    def __init__(
        self,
        parent: Optional[QWidget],
        parameter_name: str,
        config: CommonParameterWidgetConfig,
    ):
        self._config: CommonParameterWidgetConfig = config
        super().__init__(parent, parameter_name, config)

        self._layout_main = QVBoxLayout()
        self._layout_main.setContentsMargins(0, 0, 0, 0)
        self._layout_main.setSpacing(0)
        self.setLayout(self._layout_main)

        self._groupbox_container = QGroupBox(self)
        self._groupbox_container.setTitle(self.label)
        self._layout_container = QVBoxLayout()
        self._groupbox_container.setLayout(self._layout_container)
        self._layout_main.addWidget(self._groupbox_container)

        self._label_description = None
        self._checkbox_default_value = None
        self._label_parameter_error = None

        self.__build_flag: bool = False

    def build(self):
        if self.__build_flag:
            return self
        if self.description:
            self._layout_container.addWidget(self.description_label)
        self._layout_container.addWidget(self.value_widget)
        self._layout_container.addWidget(self.default_value_checkbox)
        self._layout_container.addWidget(self.parameter_error_label)
        spacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._layout_container.addSpacerItem(spacer)
        # if self.set_default_value_on_init:
        #     self.set_value(self.default_value)
        self.__build_flag = True
        return self

    def check_value_type(self, value: Any):
        pass

    def set_value(self, value: Any):
        try:
            self.check_value_type(value)
            if self._config.set_deepcopy:
                value = copy.deepcopy(value)
            if not self._check_set_value(value):
                return
            self.set_value_to_widget(value)
        except (TypeError, ValueError) as e:
            raise ParameterError(
                parameter_name=self.parameter_name,
                message=str(e),
            )

    def get_value(self) -> Any:
        if self._default_value_used():
            return self.default_value
        try:
            original_value = self.get_value_from_widget()
        except (ValueError, TypeError) as e:
            raise ParameterError(parameter_name=self.parameter_name, message=str(e))
        else:
            if self._config.get_deepcopy:
                return copy.deepcopy(original_value)
            return original_value

    @property
    def label(self) -> str:
        return super().label

    @label.setter
    def label(self, value: str):
        if self.label == value:
            return
        self._groupbox_container.setTitle(value)
        # noinspection PyUnresolvedReferences
        super(CommonParameterWidget, CommonParameterWidget).label.__set__(self, value)

    @property
    def description(self) -> str:
        return super().description

    @description.setter
    def description(self, value: str):
        if self.description == value:
            return
        self.description_label.setText(value)
        # noinspection PyUnresolvedReferences
        super(CommonParameterWidget, CommonParameterWidget).description.__set__(
            self, value
        )

    @property
    def default_value_description(self) -> str:
        return super().default_value_description

    @default_value_description.setter
    def default_value_description(self, value: str):
        if self.default_value_description == value:
            return
        self.default_value_checkbox.setText(value.format(str(self.default_value)))
        # noinspection PyUnresolvedReferences
        super(
            CommonParameterWidget, CommonParameterWidget
        ).default_value_description.__set__(self, value)

    @property
    def hide_default_value_checkbox(self) -> bool:
        if self.default_value is None:
            return False
        return self._config.hide_default_value_checkbox

    @property
    def set_default_value_on_init(self) -> bool:
        if self.default_value is not None and self.hide_default_value_checkbox:
            return True
        return self._config.set_default_value_on_init

    @property
    @abstractmethod
    def value_widget(self) -> QWidget:
        pass

    @property
    def description_label(self) -> QLabel:
        if self._label_description is not None:
            return self._label_description

        self._label_description = QLabel(self._groupbox_container)

        self._label_description.setWordWrap(True)
        self._label_description.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self._label_description.setIndent(-1)
        self._label_description.setOpenExternalLinks(True)
        # self._label_description.setStyleSheet(
        #     """QLabel{ font-weight: 300; color: #424242; }"""
        # )
        if self.description:
            self._label_description.setText(self.description)
        return self._label_description

    @property
    def default_value_checkbox(self) -> QCheckBox:
        if self._checkbox_default_value is not None:
            return self._checkbox_default_value
        self._checkbox_default_value = QCheckBox(self._groupbox_container)
        self._checkbox_default_value.setText(
            self.default_value_description.format(str(self.default_value))
        )

        def _on_toggled(checked: bool):
            if self.hide_default_value_checkbox:
                return
            self.value_widget.setEnabled(not checked)

        # noinspection PyUnresolvedReferences
        self._checkbox_default_value.toggled.connect(_on_toggled)

        if self.hide_default_value_checkbox:
            self._checkbox_default_value.setHidden(True)

        return self._checkbox_default_value

    @property
    def parameter_error_label(self) -> QLabel:
        if self._label_parameter_error is not None:
            return self._label_parameter_error
        self._label_parameter_error = QLabel(self._groupbox_container)
        self._label_parameter_error.setWordWrap(True)
        self._label_parameter_error.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )
        self._label_parameter_error.setIndent(-1)
        self._label_parameter_error.setOpenExternalLinks(True)
        self._label_parameter_error.setStyleSheet("color: red;")
        self._label_parameter_error.setHidden(True)
        return self._label_parameter_error

    def show_parameter_error(self, error: str):
        self.parameter_error_label.setText(error)
        self.parameter_error_label.setHidden(False)

    def clear_parameter_error(self):
        self.parameter_error_label.setText("")
        self.parameter_error_label.setHidden(True)

    @abstractmethod
    def set_value_to_widget(self, value: Any):
        pass

    @abstractmethod
    def get_value_from_widget(self) -> Any:
        pass

    def on_parameter_error(self, parameter_name: str, error: Any):
        if parameter_name != self.parameter_name:
            return
        error_message = str(error)
        self.show_parameter_error(error_message)

    def on_clear_parameter_error(self, parameter_name: Optional[str]):
        if parameter_name is None or parameter_name == self.parameter_name:
            self.clear_parameter_error()

    def _default_value_used(self) -> bool:
        if self.default_value_checkbox.isHidden():
            return False
        return self._checkbox_default_value.isChecked()

    def _use_default_value(self):
        if self.hide_default_value_checkbox or self.default_value_checkbox.isHidden():
            return
        self.default_value_checkbox.setChecked(True)

    # noinspection SpellCheckingInspection
    def _unuse_default_value(self):
        if self.hide_default_value_checkbox or self.default_value_checkbox.isHidden():
            return
        self.default_value_checkbox.setChecked(False)

    def _check_set_value(self, value: Any) -> bool:
        if value is None and self.default_value is not None:
            raise ValueError(
                f"None value is not allowed unless the default value is None(default_value={self.default_value})"
            )
        if value is None and self.default_value is None:
            self._use_default_value()
            return False

        if value == self.default_value:
            self._use_default_value()
        else:
            self._unuse_default_value()
        return True
