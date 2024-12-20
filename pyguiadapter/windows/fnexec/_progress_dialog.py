from typing import Optional, Literal, Tuple

from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import (
    QDialog,
    QSizePolicy,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QHBoxLayout,
)

from ...utils import to_text_format


class ProgressDialog(QDialog):
    sig_update_progress = Signal(int, str)
    sig_cancel_requested = Signal()

    def __init__(
        self,
        parent=None,
        *,
        min_value: int = 0,
        max_value: int = 100,
        inverted_appearance: bool = False,
        cancellable: bool = False,
        cancel_button_text: str = "Cancel",
        title: str = "",
        message_visible: bool = False,
        message_format: str = "%p%",
        message_centered: str = True,
        info_visible: bool = True,
        info_centered: bool = True,
        info_text_format: Literal[
            "richtext", "markdown", "plaintext", "autotext"
        ] = "autotext",
        initial_info: str = "",
        size: Tuple[int, int] = (400, 150),
        modal: bool = True,
        **kwargs
    ):
        super().__init__(parent)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._progressbar = QProgressBar(self)
        self._progressbar.setRange(min_value, max_value)
        self._progressbar.setInvertedAppearance(inverted_appearance)
        self._progressbar.setTextVisible(message_visible)
        if message_centered:
            self._progressbar.setAlignment(Qt.AlignCenter)
        self._progressbar.setFormat(message_format)
        self._layout.addWidget(self._progressbar)

        self._info_label = QLabel(self)
        if info_centered:
            self._info_label.setAlignment(Qt.AlignCenter)
        self._info_label.setWordWrap(True)
        self._info_label.setTextFormat(to_text_format(info_text_format))
        self._info_label.setVisible(info_visible)
        self._update_info(initial_info)
        self._layout.addWidget(self._info_label)

        if cancellable:
            self._button_layout = QHBoxLayout()
            self._layout.addLayout(self._button_layout)
            self._button_layout.addSpacerItem(
                QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
            )
            self._cancel_button = QPushButton(cancel_button_text, self)
            self._cancel_button.clicked.connect(self._on_cancel)
            self._button_layout.addWidget(self._cancel_button)

        self._layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

        self.sig_update_progress.connect(self._on_update_progress)

        if size:
            self.resize(*size)

        if modal:
            self.setWindowModality(Qt.ApplicationModal)
        else:
            self.setWindowModality(Qt.NonModal)

        flags = self.windowFlags()
        self.setWindowFlags(
            flags & ~Qt.WindowCloseButtonHint & ~Qt.WindowContextHelpButtonHint
        )

        self.setWindowTitle(title)

    def _update_info(self, info: Optional[str]):
        if info is None:
            return
        if not self._info_label.isVisible():
            return
        self._info_label.setText(info)

    def _on_cancel(self):
        self.sig_cancel_requested.emit()

    def _on_update_progress(self, value: int, info: str):
        self._progressbar.setValue(value)
        self._update_info(info)
