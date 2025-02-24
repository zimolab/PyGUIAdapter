import dataclasses
from typing import Literal, Optional

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel

from ....utils import to_text_format


@dataclasses.dataclass
class ProgressBarConfig(object):
    min_value: int = 0
    max_value: int = 100
    inverted_appearance: bool = False
    message_visible: bool = False
    message_centered: bool = True
    message_format: str = "%p%"
    show_info_label: bool = False
    info_text_centered: bool = False
    info_text_format: Literal["richtext", "markdown", "plaintext", "autotext"] = (
        "autotext"
    )
    initial_info: str = ""


class ProgressBar(QWidget):
    def __init__(self, parent: QWidget, config: Optional[ProgressBarConfig] = None):
        super().__init__(parent)

        self._config = None

        # noinspection PyArgumentList
        self._layout_main = QVBoxLayout()
        self._progressbar = QProgressBar(self)
        self._info_label = QLabel(self)

        self._layout_main.addWidget(self._progressbar)
        self._layout_main.addWidget(self._info_label)

        self.setLayout(self._layout_main)
        self.update_config(config)

    def update_config(self, config: Optional[ProgressBarConfig]):
        self._config = config
        if not self._config:
            self.hide()
            return
        self._progressbar.setRange(self._config.min_value, self._config.max_value)
        self._progressbar.setInvertedAppearance(self._config.inverted_appearance)
        self._progressbar.setTextVisible(self._config.message_visible)
        if self._config.message_centered:
            self._progressbar.setAlignment(Qt.AlignCenter)
        if self._config.message_format:
            self._progressbar.setFormat(self._config.message_format)
        self._info_label.setVisible(self._config.show_info_label is True)
        if self._config.info_text_centered:
            self._info_label.setAlignment(Qt.AlignCenter)
        text_format = to_text_format(self._config.info_text_format)
        self._info_label.setTextFormat(text_format)
        self._update_info(self._config.initial_info)

    def update_progress(self, current_value: int, info: Optional[str] = None):
        self._progressbar.setValue(current_value)
        self._update_info(info)

    def _update_info(self, info: Optional[str]):
        if info is None:
            return
        if not self._info_label.isVisible():
            return
        self._info_label.setText(info)
