import dataclasses
from typing import Optional, Union, Tuple, Dict

from qtpy.QtCore import Signal, QTimer, QMutex, Qt, QPropertyAnimation
from qtpy.QtWidgets import QWidget, QLabel

from .utils import move_window

DEFAULT_POSITION = (0.5, 0.9)

TextAlignment = Union[Qt.Alignment, int]
AlignCenter = Qt.AlignVCenter | Qt.AlignHCenter
AlignLeft = Qt.AlignLeft | Qt.AlignVCenter
AlignRight = Qt.AlignRight | Qt.AlignVCenter


@dataclasses.dataclass(frozen=True)
class ToastConfig(object):
    opacity: float = 0.9
    background_color: str = "#222222"
    text_color: str = "#FEFEFE"
    text_alignment: Optional[TextAlignment] = AlignCenter
    text_padding: int = 5
    font_size: int = 14
    font_family: str = "Consolas, sans-serif"
    position: Optional[Tuple[Union[int, float, None], Union[int, float, None]]] = (
        DEFAULT_POSITION
    )
    min_width: Optional[int] = 150
    min_height: Optional[int] = 100
    fade_out: Optional[int] = None
    styles: Optional[Dict[str, str]] = None


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
        if self._config.text_alignment:
            self.setAlignment(self._config.text_alignment)
        stylesheet = self._stylesheet()
        self.setStyleSheet(stylesheet)

        if self._config.fade_out:
            self._fadeout_animation = QPropertyAnimation(self, b"windowOpacity")
            self._fadeout_animation.setDuration(self._config.fade_out)
            self._fadeout_animation.setStartValue(self._config.opacity)
            self._fadeout_animation.setEndValue(0.0)
            # noinspection PyUnresolvedReferences
            self._fadeout_animation.finished.connect(self.close)

        # set window geometry
        self._set_min_size()
        self._update_size()
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
            "font-size": f"{self._config.font_size}pt",
            "font-family": f'"{self._config.font_family}"',
            "padding": f"{self._config.text_padding}",
            **more_styles,
        }

        return "\n".join(f"{k}:{v};" for k, v in style_dict.items())

    def _update_size(self):
        self.setFixedWidth(self.sizeHint().width() * 2)
        self.setFixedHeight(self.sizeHint().height() * 2)

    def _set_min_size(self):
        # text_rect = self.fontMetrics().boundingRect(self._message)
        self.setMinimumWidth(
            max(
                self._config.min_width or 0,
                self.fontMetrics().boundingRect(self._message).width() * 2,
            )
        )

        self.setMinimumHeight(
            max(
                self._config.min_height or 0,
                self.fontMetrics().boundingRect(self._message).height() * 2,
            )
        )
