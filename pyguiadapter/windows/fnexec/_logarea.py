from __future__ import annotations

import dataclasses

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QProgressBar, QLabel
from qtpy.QtGui import QTextCursor


from typing import Literal

from ... import utils

DEFAULT_LOG_OUTPUT_BACKGROUND = "#380C2A"
DEFAULT_LOG_OUTPUT_TEXT_COLOR = "#FFFFFF"
DEFAULT_LOG_OUTPUT_FONT_SIZE = 14
DEFAULT_LOG_OUTPUT_FONT_FAMILY = "Consolas, Arial, sans-serif"


@dataclasses.dataclass
class ProgressBarConfig(object):
    min_value: int = 0
    max_value: int = 100
    inverted_appearance: bool = False
    text_visible: bool = True
    text_centered: bool = True
    text_format: str = "%p%"
    message: str | None = None


@dataclasses.dataclass
class LogOutputConfig(object):
    background: str = DEFAULT_LOG_OUTPUT_BACKGROUND
    text_color: str = DEFAULT_LOG_OUTPUT_TEXT_COLOR
    font_size: int = DEFAULT_LOG_OUTPUT_FONT_SIZE
    font_family: str = DEFAULT_LOG_OUTPUT_FONT_FAMILY
    line_wrap_mode: Literal[
        "no_wrap",
        "widget_width",
        "fixed_pixel_width",
        "fixed_column_width",
    ] = "widget_width"
    word_wrap_mode: Literal[
        "no_wrap",
        "word_wrap",
        "manual_wrap",
        "wrap_anywhere",
        "wrap_at_word_boundary_or_anywhere",
    ] = "word_wrap"
    fixed_line_wrap_width: int = 80


class ProgressBar(QWidget):
    def __init__(self, parent: QWidget, config: ProgressBarConfig | None = None):
        super().__init__(parent)
        self._config = None

        self._vlayout_main = QVBoxLayout(self)
        self._progressbar = QProgressBar(self)
        self._label_message = QLabel(self)
        self._vlayout_main.addWidget(self._progressbar)
        self._vlayout_main.addWidget(self._label_message)

        self.update_config(config)

    def update_config(self, config: ProgressBarConfig):
        self._config = config
        if not self._config:
            return
        self._progressbar.setRange(self._config.min_value, self._config.max_value)
        self._progressbar.setInvertedAppearance(self._config.inverted_appearance)
        self._progressbar.setTextVisible(self._config.text_visible)
        if self._config.text_centered:
            self._progressbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self._config.text_format:
            self._progressbar.setFormat(self._config.text_format)
        if self._config.message:
            self._label_message.setText(self._config.message)

    def update_progress(self, current_value: int, message: str | None = None):
        self._progressbar.setValue(current_value)
        if message:
            self._label_message.setText(message)


class FnExecuteLogOutputArea(QWidget):
    def __init__(
        self,
        parent: QWidget,
        progressbar_config: ProgressBarConfig | None,
        log_output_config: LogOutputConfig,
    ):
        super().__init__(parent)

        self._vlayout_main = QVBoxLayout(self)
        self._vlayout_main.setContentsMargins(1, 2, 1, 2)
        self._setup_log_output(log_output_config)
        self._setup_progressbar(progressbar_config)

    def show_progressbar(self):
        self._progressbar.show()

    def hide_progressbar(self):
        self._progressbar.hide()

    def update_progressbar_config(self, config: ProgressBarConfig):
        self._progressbar.update_config(config)

    def update_progress(self, current_value: int, message: str | None = None):
        self._progressbar.update_progress(current_value, message)

    def clear_log_output(self):
        self._textbrowser_log_output.clear()

    def append_log_output(self, log_text: str, html: bool = False):
        if log_text and not html:
            self._textbrowser_log_output.insertPlainText(log_text)
            return
        cursor: QTextCursor = self._textbrowser_log_output.textCursor()
        if log_text:
            cursor.insertHtml(f"<div>{log_text}</div>")
        cursor.insertHtml("<br>")
        self._textbrowser_log_output.ensureCursorVisible()
        self._textbrowser_log_output.moveCursor(QTextCursor.MoveOperation.End)

    def _setup_log_output(self, config: LogOutputConfig | None):
        self._log_output_config = config or LogOutputConfig()
        self._textbrowser_log_output = QTextBrowser(self)
        utils.set_textbrowser_wrap_mode(
            self._textbrowser_log_output,
            word_wrap_mode=self._log_output_config.word_wrap_mode,
            line_wrap_mode=self._log_output_config.line_wrap_mode,
            fixed_line_wrap_width=self._log_output_config.fixed_line_wrap_width,
        )

        stylesheet = utils.get_textbrowser_stylesheet(
            bg_color=self._log_output_config.background,
            text_color=self._log_output_config.text_color,
            font_size=self._log_output_config.font_size,
            font_family=self._log_output_config.font_family,
        )
        self._textbrowser_log_output.setStyleSheet(stylesheet)
        self._vlayout_main.addWidget(self._textbrowser_log_output)

    def _setup_progressbar(self, config: ProgressBarConfig | None):
        self._progressbar = ProgressBar(self, config=config)
        self._vlayout_main.addWidget(self._progressbar)
