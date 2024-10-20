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

from ..constants.color import COLOR_FATAL, COLOR_REGULAR_TEXT
from ..constants.font import FONT_SMALL
from ..exceptions import ParameterError
from ..paramwidget import BaseParameterWidgetConfig, BaseParameterWidget


@dataclasses.dataclass(frozen=True)
class CommonParameterWidgetConfig(BaseParameterWidgetConfig):
    """
    通用参数控件配置类。继承自 `BaseParameterWidgetConfig` 类。是所有通用参数控件的配置基类。
    """

    set_default_value_on_init: bool = True
    """
    是否在控件初始化时设置默认值。默认为 `True`。
    """

    hide_default_value_checkbox: bool = True
    """是否隐藏默认值复选框。当default_value为None时，此选项无效，默认值复选框始终显示。"""

    set_deepcopy: bool = True
    get_deepcopy: bool = True

    description_font_size: Optional[int] = FONT_SMALL
    """控件描述文本字体大小。默认为 `FONT_SMALL`。"""

    description_color: Optional[str] = COLOR_REGULAR_TEXT
    """控件描述文本颜色。默认为 `COLOR_REGULAR_TEXT`。"""

    parameter_error_font_size: Optional[int] = FONT_SMALL
    """ParameterError文本字体大小。默认为 `FONT_SMALL`。"""

    parameter_error_color: Optional[str] = COLOR_FATAL
    """ParameterError文本颜色。默认为 `COLOR_FATAL`。"""

    @classmethod
    def target_widget_class(cls) -> Type["CommonParameterWidget"]:
        return CommonParameterWidget


class CommonParameterWidget(BaseParameterWidget):
    """
    通用参数控件基类。继承自 `BaseParameterWidget` 类。为所有参数控件定义了基本的布局和整体外观。目前内置控件均继承自此类。
    """

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
        self._layout_container.addSpacerItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
        )
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
            raise ParameterError(parameter_name=self.parameter_name, message=str(e))

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
        """
        返回“值控件”。此为抽象方法，必须在子类中实现。

        Returns:
            控件示例。
        """
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
        if self._config.description_color:
            self._label_description.setStyleSheet(
                f'color: "{self._config.description_color}"'
            )
        if self._config.description_font_size:
            font = self._label_description.font()
            font.setPixelSize(self._config.description_font_size)
            self._label_description.setFont(font)

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
        if self._config.parameter_error_color:
            self._label_parameter_error.setStyleSheet(
                f'color: "{self._config.parameter_error_color}"'
            )
        if self._config.parameter_error_font_size:
            font = self._label_parameter_error.font()
            font.setPixelSize(self._config.parameter_error_font_size)
            self._label_parameter_error.setFont(font)
        self._label_parameter_error.setIndent(-1)
        self._label_parameter_error.setOpenExternalLinks(True)
        self._label_parameter_error.setHidden(True)
        return self._label_parameter_error

    def show_parameter_error(self, error: str):
        self.parameter_error_label.setText(error)
        self.parameter_error_label.setHidden(False)

    def clear_parameter_error(self):
        self.parameter_error_label.setText("")
        self.parameter_error_label.setHidden(True)

    @abstractmethod
    def set_value_to_widget(self, value: Any) -> None:
        """
        将用户传入的值设置到“值控件”中。此为抽象方法，必须在子类中实现。

        Args:
            value: 用户传入的值

        Returns:
            无返回值
        """
        pass

    @abstractmethod
    def get_value_from_widget(self) -> Any:
        """
        从“值控件”中获取用户当前输入的值。此为抽象方法，必须在子类中实现。

        Returns:
            用户当前输入的值
        """
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
                f"None value is not allowed unless the default_value is None(default_value={self.default_value})"
            )
        if value is None and self.default_value is None:
            self._use_default_value()
            return False

        if value == self.default_value:
            self._use_default_value()
        else:
            self._unuse_default_value()
        return True
