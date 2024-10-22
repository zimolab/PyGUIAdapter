import dataclasses

from qtpy.QtCore import QRegularExpression, Qt
from qtpy.QtGui import QValidator, QRegularExpressionValidator
from qtpy.QtWidgets import QWidget, QLineEdit
from typing import Type, Optional, Union

from ..common import CommonParameterWidget, CommonParameterWidgetConfig


EchoMode = QLineEdit.EchoMode
"""LineEdit的回显模式"""

Alignment = Qt.AlignmentFlag
"""LineEdit中的对齐方式"""


@dataclasses.dataclass(frozen=True)
class LineEditConfig(CommonParameterWidgetConfig):
    """LineEdit配置类"""

    default_value: Optional[str] = ""
    """默认值"""

    placeholder: str = ""
    """占位文本，输入框为空时将显示该文本"""

    clear_button: bool = False
    """是否显示清除按钮"""

    echo_mode: Optional[EchoMode] = None
    """回显模式，默认为Normal"""

    alignment: Optional[Alignment] = None
    """输入文本的对齐方式，默认为AlignLeft"""

    input_mask: Optional[str] = None
    """输入掩码，用于限制用户输入，可以参考：https://doc.qt.io/qt-5/qlineedit.html#inputMask-prop"""

    max_length: Optional[int] = None
    """最大长度"""

    validator: Union[QValidator, str, None] = None
    """输入验证器，可以是QValidator对象，也可以是正则表达式字符串，默认无验证器"""

    drag_enabled: bool = True
    """是否允许拖拽"""

    frame: bool = True
    """是否显示边框"""

    readonly: bool = False
    """是否只读"""

    @classmethod
    def target_widget_class(cls) -> Type["LineEdit"]:
        return LineEdit


class LineEdit(CommonParameterWidget):
    ConfigClass = LineEditConfig

    PasswordEchoMode = EchoMode.Password
    """回显模式：显示为密码"""

    PasswordEchoOnEditMode = EchoMode.PasswordEchoOnEdit
    """回显模式：输入时正常显示，输入结束后显示为密码"""

    NormalEchoMode = EchoMode.Normal
    """回显模式：正常显示"""

    NoEchoMode = EchoMode.NoEcho
    """回显模式：隐藏输入内容"""

    AlignLeft = Alignment.AlignRight
    """文本对齐方式：左对齐"""

    AlignRight = Alignment.AlignRight
    """文本对齐方式：右对齐"""

    AlignCenter = Alignment.AlignCenter
    """文本对齐方式：居中对齐"""

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: LineEditConfig
    ):

        self._value_widget: Optional[QLineEdit] = None
        super().__init__(parent, parameter_name, config)

    @property
    def value_widget(self) -> QLineEdit:
        if self._value_widget is None:
            config: LineEditConfig = self.config
            self._value_widget = QLineEdit("", self)
            self._value_widget.setPlaceholderText(config.placeholder or "")
            self._value_widget.setClearButtonEnabled(config.clear_button)
            if config.echo_mode is not None:
                self._value_widget.setEchoMode(config.echo_mode)

            if config.input_mask:
                self._value_widget.setInputMask(config.input_mask)

            max_length = config.max_length
            if isinstance(max_length, int):
                max_length = max(max_length, 1)
                self._value_widget.setMaxLength(max_length)

            validator = config.validator
            if isinstance(validator, str):
                regex = QRegularExpression(validator)
                validator = QRegularExpressionValidator(self._value_widget)
                validator.setRegularExpression(regex)
            assert isinstance(validator, (QValidator, type(None)))
            if validator:
                self._value_widget.setValidator(validator)

            if config.alignment is not None:
                self._value_widget.setAlignment(config.alignment)

            self._value_widget.setFrame(config.frame is True)
            self._value_widget.setDragEnabled(config.drag_enabled is True)
            self._value_widget.setReadOnly(config.readonly is True)

        return self._value_widget

    def set_value_to_widget(self, value: str):
        self.value_widget.setText(str(value))

    def get_value_from_widget(self) -> str:
        if not self._value_widget.hasAcceptableInput():
            raise ValueError("unacceptable input: validation failed")
        return self.value_widget.text()
