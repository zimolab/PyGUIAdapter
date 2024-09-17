from __future__ import annotations

import dataclasses
from typing import Literal

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel

_FORMATS = {
    "richtext": Qt.TextFormat.RichText,
    "markdown": Qt.TextFormat.MarkdownText,
    "plaintext": Qt.TextFormat.PlainText,
    "autotext": Qt.TextFormat.AutoText,
}


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
    def __init__(self, parent: QWidget, config: ProgressBarConfig | None = None):
        super().__init__(parent)

        self._config = None

        # noinspection PyArgumentList
        self._layout_main = QVBoxLayout(self)
        self._progressbar = QProgressBar(self)
        self._info_label = QLabel(self)

        self._layout_main.addWidget(self._progressbar)
        self._layout_main.addWidget(self._info_label)

        self.update_config(config)

    def update_config(self, config: ProgressBarConfig):
        self._config = config
        if not self._config:
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
        text_format = _FORMATS.get(
            self._config.info_text_format, Qt.TextFormat.AutoText
        )
        self._info_label.setTextFormat(text_format)
        self._update_info(self._config.initial_info)

    def update_progress(self, current_value: int, info: str | None = None):
        self._progressbar.setValue(current_value)
        self._update_info(info)

    def _update_info(self, info: str | None):
        if info is None:
            return
        if not self._info_label.isVisible():
            return
        self._info_label.setText(info)
