from abc import abstractmethod
from typing import Optional, Any, Tuple

from qtpy.QtWidgets import QDialog, QWidget, QPushButton, QVBoxLayout, QHBoxLayout

from ._ui import IconType, get_icon


class BaseCustomDialog(QDialog):
    def __init__(self, parent: Optional[QWidget], **kwargs):
        super().__init__(parent)

    @abstractmethod
    def get_result(self) -> Any:
        pass

    @classmethod
    def new_instance(cls, parent: QWidget, **kwargs) -> "BaseCustomDialog":
        return cls(parent, **kwargs)


class UniversalInputDialog(BaseCustomDialog):
    def __init__(
        self,
        parent: Optional[QWidget],
        title: str = "",
        icon: IconType = None,
        size: Tuple[int, int] = (400, 300),
        ok_button_text: str = "Ok",
        cancel_button_text: Optional[str] = "Cancel",
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        self._title = title or ""
        self._icon = icon
        self._size = size
        self._ok_button_text: str = ok_button_text
        self._cancel_button_text: Optional[str] = cancel_button_text

        self._layout: QVBoxLayout = QVBoxLayout(self)
        self._main_widget: Optional[QWidget] = None
        self._ok_button: QPushButton = QPushButton(self)
        self._cancel_button: Optional[QPushButton] = None

        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle(self._title)
        icon = get_icon(self._icon)
        if icon:
            self.setWindowIcon(icon)
        if self._size:
            self.resize(*self._size)
        if self._main_widget is None:
            main_widget = self.create_main_widget()
            main_widget.setParent(self)
            self._main_widget = main_widget
        self._layout.addWidget(self._main_widget)
        self._setup_buttons()

    @abstractmethod
    def create_main_widget(self) -> QWidget:
        pass

    def _setup_buttons(self):
        self._ok_button.setText(self._ok_button_text)
        # noinspection PyUnresolvedReferences
        self._ok_button.clicked.connect(self.on_accept)
        if self._cancel_button_text:
            self._cancel_button = QPushButton(self)
            self._cancel_button.setText(self._cancel_button_text)
            # noinspection PyUnresolvedReferences
            self._cancel_button.clicked.connect(self.on_reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self._ok_button)
        if self._cancel_button_text:
            button_layout.addWidget(self._cancel_button)
        self._layout.addLayout(button_layout)

    def on_accept(self):
        self.accept()

    def on_reject(self):
        self.reject()

    @abstractmethod
    def get_result(self) -> Any:
        pass

    @classmethod
    def new_instance(cls, parent: QWidget, **kwargs) -> "UniversalInputDialog":
        return super().new_instance(parent, **kwargs)
