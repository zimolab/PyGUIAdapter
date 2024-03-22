import dataclasses
from typing import Type, Any, Callable, Optional, List, Dict

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
)
from function2widgets.description import FunctionDescription
from function2widgets.widget import BaseParameterWidget

from pyguiadapter.commons import (
    T,
    clear_layout,
    get_widget_factory,
    get_function_parser,
)
from pyguiadapter.interact import upopup
from pyguiadapter.interact.upopup import UPopup
from pyguiadapter.ui.config import WindowConfig
from pyguiadapter.ui.generated.ui_initialization_window import Ui_InitializationWindow


@dataclasses.dataclass
class InitializationWindowConfig(WindowConfig):
    label_text: Optional[str] = None
    button_text: Optional[str] = None

    def apply_to(self, w: "InitializationWindow") -> None:
        super().apply_to(w)
        if self.label_text is not None:
            w.set_label_text(self.label_text)
        if self.button_text is not None:
            w.set_button_text(self.button_text)


class InitializationWindow(QDialog):
    def __init__(
        self,
        klass: Type[T],
        window_config: InitializationWindowConfig = None,
        window_created_callback: Optional[
            Callable[["InitializationWindow"], None]
        ] = None,
        parent=None,
    ):
        window_config = window_config or InitializationWindowConfig()

        super().__init__(parent=parent)

        self._class: Type[T] = klass
        self._class_instance: Optional[T] = None
        self._parameter_widgets: List[BaseParameterWidget] = []
        self._layout_parameter_widgets = QVBoxLayout()

        self._window_create_callback = window_created_callback

        self._ui = Ui_InitializationWindow()
        self._window_config: InitializationWindowConfig = window_config

        self._upopup = UPopup(self)

        self._setup_ui()
        self.window_config = window_config

        self._setup_parameter_widgets()

        upopup.set_current_window(self)

        if self._window_create_callback is not None:
            self._window_create_callback(self)

    @property
    def popup(self) -> UPopup:
        return self._upopup

    @property
    def window_config(self) -> InitializationWindowConfig:
        return self._window_config

    @window_config.setter
    def window_config(self, window_config: InitializationWindowConfig):
        if not isinstance(window_config, InitializationWindowConfig):
            raise TypeError(
                f"window_config must be an instance of InitializationWindowConfig, got {type(window_config)}"
            )
        self._window_config = window_config
        self._window_config.apply_to(self)

    def set_label_text(self, text: str):
        self._ui.label.setText(text)

    def set_button_text(self, text: str):
        self._ui.button_initialize.setText(text)

    def get_class_instance(self) -> Optional[T]:
        return self._class_instance

    @classmethod
    def initialize_class(
        cls,
        klass: Type[T],
        window_config: InitializationWindowConfig = None,
        window_created_callback: Optional[
            Callable[["InitializationWindow"], None]
        ] = None,
        parent=None,
    ) -> Optional[T]:
        _window = cls(
            klass=klass,
            window_config=window_config,
            window_created_callback=window_created_callback,
            parent=parent,
        )
        ret = _window.exec()
        if ret == QDialog.DialogCode.Accepted:
            _instance = _window.get_class_instance()
        else:
            _instance = None
        return _instance

    def _setup_ui(self):
        self._ui.setupUi(self)
        self._layout_parameter_widgets.setParent(self._ui.param_widgets_container)
        self._ui.param_widgets_container.setLayout(self._layout_parameter_widgets)

        self._ui.button_initialize.clicked.connect(self._do_initialization)

    def _do_initialization(self):
        arguments = self._get_arguments()
        try:
            self._class_instance = self._class(**arguments)
            self.accept()
        except BaseException as e:
            self._class_instance = None
            msg = self.tr(f"Failed to initialize class {self._class}!\n\nError: \n{e}")
            QMessageBox.critical(self, self.tr("Error"), msg)
            return

    def _setup_parameter_widgets(self):
        self._cleanup_parameter_widgets()
        clear_layout(self._layout_parameter_widgets)
        parser = get_function_parser()
        constructor_description = parser.parse(
            func=self._class, parse_class=True, ignore_self_param=True
        )
        self._create_parameter_widgets(constructor_description)
        self._add_parameter_widgets()

    def _create_parameter_widgets(self, function_description: FunctionDescription):
        factory = get_widget_factory()
        try:
            for parameter_description in function_description.parameters:
                parameter_widget = factory.create_widget_from_description(
                    parameter_description
                )
                self._parameter_widgets.append(parameter_widget)
        except BaseException as e:
            self._cleanup_parameter_widgets()
            raise e

    def _add_parameter_widgets(self):
        for widget in self._parameter_widgets:
            self._layout_parameter_widgets.addWidget(widget)
        spacer_item = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._layout_parameter_widgets.addSpacerItem(spacer_item)

    def _cleanup_parameter_widgets(self):
        for widget in self._parameter_widgets:
            widget.deleteLater()
        self._parameter_widgets.clear()

    def _get_arguments(self) -> Dict[str, Any]:
        return {
            param_widget.parameter_name: param_widget.get_value()
            for param_widget in self._parameter_widgets
        }
