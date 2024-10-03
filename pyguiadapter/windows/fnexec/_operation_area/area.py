from typing import Optional

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout

from ....utils import hline
from .._base import FnExecuteWindowConfig


class OperationArea(QWidget):
    sig_execute_requested = Signal()
    sig_cancel_requested = Signal()
    sig_clear_requested = Signal()

    def __init__(self, parent: Optional[QWidget], config: FnExecuteWindowConfig):
        self._config: FnExecuteWindowConfig = config
        self._layout: Optional[QVBoxLayout] = None
        self._button_layout: Optional[QHBoxLayout] = None
        self._execute_button: Optional[QPushButton] = None
        self._clear_button: Optional[QPushButton] = None
        self._cancel_button: Optional[QPushButton] = None
        self._clear_checkbox: Optional[QCheckBox] = None

        super().__init__(parent)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._button_layout = QHBoxLayout()

        self._execute_button = QPushButton(self)
        self._cancel_button = QPushButton(self)
        self._clear_button = QPushButton(self)
        self._clear_checkbox = QCheckBox(self)

        self._button_layout.addWidget(self._execute_button)
        self._button_layout.addWidget(self._cancel_button)
        self._button_layout.addWidget(self._clear_button)

        self._layout.addWidget(self._clear_checkbox)
        self._layout.addWidget(hline(self))
        self._layout.addLayout(self._button_layout)

        self._execute_button.clicked.connect(self.sig_execute_requested)
        self._cancel_button.clicked.connect(self.sig_cancel_requested)
        self._clear_button.clicked.connect(self.sig_clear_requested)

        self.setLayout(self._layout)

    def apply_config(self):
        self._execute_button.setText(self._config.execute_button_text or "Execute")
        self._cancel_button.setText(self._config.cancel_button_text or "Cancel")
        self._clear_button.setText(self._config.clear_button_text or "Clear")
        self._clear_checkbox.setText(self._config.clear_checkbox_text or "clear output")

        self._clear_button.setVisible(self._config.show_clear_checkbox)
        self._clear_checkbox.setVisible(self._config.show_clear_checkbox)

        self._clear_checkbox.setChecked(self._config.enable_auto_clear)

    def set_execute_button_enabled(self, enabled: bool):
        if self._execute_button is not None:
            self._execute_button.setEnabled(enabled)

    def set_clear_button_enabled(self, enabled: bool):
        if self._clear_button is not None:
            self._clear_button.setEnabled(enabled)

    def set_cancel_button_enabled(self, enabled: bool):
        if self._cancel_button is not None:
            self._cancel_button.setEnabled(enabled)

    def set_clear_button_visible(self, visible: bool):
        if self._clear_button is not None:
            self._config.show_clear_button = visible
            self._clear_button.setVisible(visible)

    def set_cancel_button_visible(self, visible: bool):
        if self._cancel_button is not None:
            self._cancel_button.setVisible(visible)

    def set_clear_checkbox_visible(self, visible: bool):
        if self._clear_checkbox is not None:
            self._config.show_clear_checkbox = visible
            self._clear_checkbox.setVisible(visible)

    def is_clear_checkbox_checked(self) -> bool:
        return self._clear_checkbox.isChecked()
