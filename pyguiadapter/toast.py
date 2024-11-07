"""
@Time    : 2024.10.20
@File    : toast.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 实现了简单的toast提示框
"""

import dataclasses
from typing import Optional, Union, Tuple, Dict, Sequence

from qtpy.QtCore import Signal, QTimer, QMutex, Qt, QPropertyAnimation
from qtpy.QtWidgets import QWidget, QLabel

from .constants.font import FONT_FAMILY
from .constants.color import COLOR_TOAST_BACKGROUND_CLASSIC, COLOR_TOAST_TEXT_CLASSIC
from .utils import move_window

DEFAULT_POSITION = (0.5, 0.9)

TextAlignment = Union[Qt.AlignmentFlag, int]
"""文字对齐方式"""

AlignCenter = Qt.AlignVCenter | Qt.AlignHCenter
"""居中对齐"""

AlignLeft = Qt.AlignLeft | Qt.AlignVCenter
"""左对齐"""

AlignRight = Qt.AlignRight | Qt.AlignVCenter
"""右对齐"""


@dataclasses.dataclass(frozen=True)
class ToastConfig(object):
    """
    Toast控件配置类
    """

    opacity: float = 0.9
    """不透明度"""

    background_color: str = COLOR_TOAST_BACKGROUND_CLASSIC
    """背景颜色"""

    text_color: str = COLOR_TOAST_TEXT_CLASSIC
    """文字颜色"""

    text_padding: int = 50
    """文字边距"""

    text_alignment: Optional[TextAlignment] = None
    """文字对齐方式"""

    font_family: Union[Sequence[str], str] = FONT_FAMILY
    """字体"""

    font_size: int = 26
    """字体大小"""

    position: Optional[Tuple[Union[int, float, None], Union[int, float, None]]] = (
        DEFAULT_POSITION
    )
    """显示位置，可以使用百分比或绝对坐标，比如`(0.5, 0.5)`表示在屏幕中心显示，`(100, 100)`表示在屏幕坐标x=100 y=100处显示"""

    fixed_size: Optional[Tuple[int, int]] = None
    """固定尺寸"""

    fade_out: Optional[int] = None
    """淡出时间"""

    styles: Optional[Dict[str, str]] = None
    """额外样式"""


class ToastWidget(QLabel):
    sig_toast_finished = Signal()

    def __init__(
        self,
        parent: Optional[QWidget],
        message: str,
        duration: int,
        config: Optional[ToastConfig] = None,
    ):
        super().__init__(parent)
        self._message: str = message
        self._duration: int = duration
        self._config: ToastConfig = config or ToastConfig()

        self._lock = QMutex()
        self._closing: bool = False

        self._fadeout_animation: Optional[QPropertyAnimation] = None
        if self._config.fade_out:
            self._fadeout_animation = QPropertyAnimation(self, b"windowOpacity")
            self._fadeout_animation.setDuration(self._config.fade_out)
            self._fadeout_animation.setStartValue(self._config.opacity)
            self._fadeout_animation.setEndValue(0.0)
            # noinspection PyUnresolvedReferences
            self._fadeout_animation.finished.connect(self.close)

        self._setup_ui()

        self._close_timer: Optional[QTimer] = None
        if self._duration > 0:
            self._close_timer = QTimer(self)
            self._close_timer.setSingleShot(True)
            # noinspection PyUnresolvedReferences
            self._close_timer.timeout.connect(self._on_finish)

        self.hide()

    def _setup_ui(self):
        # set message text
        self.setText(self._message)

        # set window attributes
        flags = self.windowFlags()
        flags |= Qt.Window
        flags |= Qt.WindowStaysOnTopHint
        flags |= Qt.FramelessWindowHint
        flags |= Qt.WindowTransparentForInput
        self.setWindowFlags(flags)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.setWordWrap(True)
        stylesheet = self._stylesheet()
        self.setStyleSheet(stylesheet)

        if self._config.text_alignment:
            self.setAlignment(self._config.text_alignment)
        if self._config.fixed_size:
            self.setFixedSize(self._config.fixed_size[0], self._config.fixed_size[1])
        else:
            self.adjustSize()

        move_window(self, *self._config.position)
        self.setWindowOpacity(self._config.opacity)

    def start(self):
        self.show()
        if self._close_timer:
            self._close_timer.start(self._duration)

    def finish(self):
        if self._close_timer:
            self._close_timer.stop()
        self._on_finish()

    def _on_finish(self):
        self._lock.lock()

        if self._closing:
            self._lock.unlock()
            return
        self._closing = True
        self._lock.unlock()
        if self._fadeout_animation:
            self._fadeout_animation.start()
        else:
            self.hide()
            self.close()

    def closeEvent(self, event):
        self._lock.lock()
        if not self._closing:
            event.ignore()
            self._lock.unlock()
            return
        self._lock.unlock()
        # noinspection PyUnresolvedReferences
        self._close_timer.timeout.disconnect(self._on_finish)
        if self._fadeout_animation:
            # noinspection PyUnresolvedReferences
            self._fadeout_animation.finished.disconnect(self.close)
        event.accept()
        # noinspection PyUnresolvedReferences
        self.sig_toast_finished.emit()

    def _stylesheet(self) -> str:
        more_styles = self._config.styles or {}
        style_dict = {
            "background-color": f'"{self._config.background_color}"',
            "color": f'"{self._config.text_color}"',
            "font-size": f"{self._config.font_size}px",
            "font-family": f'"{self._config.font_family}"',
            "padding": f"{self._config.text_padding}",
            **more_styles,
        }

        return "\n".join(f"{k}:{v};" for k, v in style_dict.items())
