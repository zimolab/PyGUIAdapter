from __future__ import annotations

import dataclasses

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel


@dataclasses.dataclass
class ProgressBarConfig(object):
    min_value: int = 0
    max_value: int = 100
    inverted_appearance: bool = False
    text_visible: bool = True
    text_centered: bool = True
    text_format: str = "%p%"
    message: str | None = None


class ProgressBar(QWidget):
    def __init__(self, parent: QWidget, config: ProgressBarConfig | None = None):
        super().__init__(parent)

        self._config = None

        # noinspection PyArgumentList
        self._layout_main = QVBoxLayout(self)
        self._progressbar = QProgressBar(self)
        self._message_label = QLabel(self)

        self._layout_main.addWidget(self._progressbar)
        self._layout_main.addWidget(self._message_label)

        self.update_config(config)

    def update_config(self, config: ProgressBarConfig):
        self._config = config
        if not self._config:
            return
        self._progressbar.setRange(self._config.min_value, self._config.max_value)
        self._progressbar.setInvertedAppearance(self._config.inverted_appearance)
        self._progressbar.setTextVisible(self._config.text_visible)
        if self._config.text_centered:
            self._progressbar.setAlignment(Qt.AlignCenter)
        if self._config.text_format:
            self._progressbar.setFormat(self._config.text_format)
        if self._config.message:
            self._message_label.setText(self._config.message)

    def update_progress(self, current_value: int, message: str | None = None):
        self._progressbar.setValue(current_value)
        if message:
            self._message_label.setText(message)
