import dataclasses
from typing import Type, Any, Callable, Optional, List, Dict

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
)
from function2widgets.info import FunctionInfo
from function2widgets.widget import BaseParameterWidget

from pyguiadapter.commons import (
    T,
    clear_layout,
    get_param_widget_factory,
    get_function_parser,
)
from pyguiadapter.interact import upopup
from pyguiadapter.interact.upopup import UPopup
from pyguiadapter.ui.config import WindowConfig
from pyguiadapter.ui.generated.ui_class_init_window import Ui_ClassInitWindow


@dataclasses.dataclass
class ClassInitWindowConfig(WindowConfig):
    title_label_text: Optional[str] = None
    init_button_text: Optional[str] = None


class ClassInitWindow(QDialog):
    def __init__(
        self,
        klass: Type[T],
        config: ClassInitWindowConfig = None,
        callback_window_created: Optional[Callable[["ClassInitWindow"], None]] = None,
        parent=None,
    ):
        config = config or ClassInitWindowConfig()

        super().__init__(parent=parent)

        self._callback_window_created = callback_window_created
        self._config: ClassInitWindowConfig = config

        self._class: Type[T] = klass
        self._class_instance: Optional[T] = None

        self._param_widgets: List[BaseParameterWidget] = []
        self._layout_param_widgets = QVBoxLayout()
        self._ui = Ui_ClassInitWindow()

        self._upopup = UPopup(self)
        upopup.set_current_window(self)
        self.window_config = config
        self._setup_ui()
        self._setup_parameter_widgets()

        if self._callback_window_created is not None:
            self._callback_window_created(self)

    @property
    def popup(self) -> UPopup:
        return self._upopup

    @property
    def window_config(self) -> ClassInitWindowConfig:
        return self._config

    @window_config.setter
    def window_config(self, config: ClassInitWindowConfig):
        if not isinstance(config, ClassInitWindowConfig):
            raise TypeError(
                f"window_config must be an instance of InitializationWindowConfig, got {type(config)}"
            )
        self._config = config
        self._config.apply_basic_configs(self)

    def get_class_instance(self) -> Optional[T]:
        return self._class_instance

    @classmethod
    def initialize_class(
        cls,
        klass: Type[T],
        config: ClassInitWindowConfig = None,
        callback_window_created: Optional[Callable[["ClassInitWindow"], None]] = None,
        parent=None,
    ) -> Optional[T]:
        _window = cls(
            klass=klass,
            config=config,
            callback_window_created=callback_window_created,
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
        self._layout_param_widgets.setParent(self._ui.param_widgets_container)
        self._ui.param_widgets_container.setLayout(self._layout_param_widgets)

        button_text = self.window_config.init_button_text
        if button_text:
            self._ui.button_initialize.setText(button_text)
        self._ui.button_initialize.clicked.connect(self._do_class_init)

        label_text = self.window_config.title_label_text
        if label_text:
            self._ui.label_title.setText(label_text)

    def _do_class_init(self):
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
        self._cleanup_param_widgets()
        clear_layout(self._layout_param_widgets)
        parser = get_function_parser()
        init_func_info = parser.parse(func_obj=self._class, ignore_self_param=True)
        self._create_param_widgets(init_func_info)
        self._add_param_widgets()

    def _create_param_widgets(self, function_info: FunctionInfo):
        factory = get_param_widget_factory()
        try:
            for param_info in function_info.parameters:
                param_widget = factory.create_widget_for_parameter(param_info)
                self._param_widgets.append(param_widget)
        except BaseException as e:
            self._cleanup_param_widgets()
            raise e

    def _add_param_widgets(self):
        for widget in self._param_widgets:
            self._layout_param_widgets.addWidget(widget)
        spacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._layout_param_widgets.addSpacerItem(spacer)

    def _cleanup_param_widgets(self):
        for widget in self._param_widgets:
            widget.deleteLater()
        self._param_widgets.clear()

    def _get_arguments(self) -> Dict[str, Any]:
        return {
            param_widget.parameter_name: param_widget.get_value()
            for param_widget in self._param_widgets
        }
