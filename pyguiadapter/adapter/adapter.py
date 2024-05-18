import contextlib
import inspect
import sys
from typing import Type, Optional, List, Dict, Callable, Union

from PyQt6.QtWidgets import QApplication, QMessageBox, QStyleFactory
from function2widgets import CommonParameterWidgetArgs


from pyguiadapter.commons import T, DocumentFormat
from pyguiadapter.exceptions import (
    AlreadyExistsError,
    NotExistError,
    AppNotStartedError,
    ClassInitCancelled,
)
from pyguiadapter.ui.window.class_init import ClassInitWindow, ClassInitWindowConfig
from pyguiadapter.ui.window.func_execution import ExecutionWindow, ExecutionWindowConfig
from pyguiadapter.ui.window.func_selection import SelectionWindow, SelectionWindowConfig
from pyguiadapter.ui.menus import ActionItem, Separator

from .bundle import FunctionBundle
from .constants import (
    ALWAYS_SHOW_SELECTION_WINDOW,
    AS_IS,
    _KEY_WIDGET_ARGS,
    CANCEL_EVENT_PARAM_NAME,
    DEFAULT_APP_STYLE,
)
from ..progressbar_config import ProgressBarConfig


class GUIAdapter:
    def __init__(
        self,
        argv: List[str] = None,
        *,
        config_class_init_window: Optional[ClassInitWindowConfig] = None,
        config_selection_window: Optional[SelectionWindowConfig] = None,
        config_execution_window: Optional[ExecutionWindowConfig] = None,
        callback_app_started: Optional[Callable[[QApplication], None]] = None,
        callback_class_init_window_created: Optional[
            Callable[[ClassInitWindow], None]
        ] = None,
        callback_selection_window_created: Optional[
            Callable[[SelectionWindow], None]
        ] = None,
        callback_execution_window_created: Optional[
            Callable[[ExecutionWindow], None]
        ] = None,
        always_show_selection_window: bool = ALWAYS_SHOW_SELECTION_WINDOW,
        app_style: Optional[str] = DEFAULT_APP_STYLE,
    ):
        if argv is None:
            argv = sys.argv

        self._argv = argv
        self._config_class_init_window = (
            config_class_init_window or ClassInitWindowConfig()
        )
        self._config_selection_window = (
            config_selection_window or SelectionWindowConfig()
        )
        self._config_execution_window = (
            config_execution_window or ExecutionWindowConfig()
        )

        self._callback_app_started = callback_app_started
        self._callback_execution_window_created = callback_execution_window_created
        self._callback_class_init_window_created = callback_class_init_window_created
        self._callback_selection_window_created = callback_selection_window_created

        self._app_style = app_style

        self.always_show_selection_window = always_show_selection_window

        self._func_bundles = {}
        self._application: Optional[QApplication] = None

        self._selection_window: Optional[SelectionWindow] = None
        self._execution_window: Optional[ExecutionWindow] = None

    def add(
        self,
        func_obj: callable,
        bind: T = None,
        display_name: str = None,
        display_icon: str = None,
        display_document: str = None,
        document_format: DocumentFormat = DocumentFormat.PLAIN,
        widget_configs: Optional[Dict[str, Dict]] = None,
        cancelable: bool = False,
        cancel_event_param_name: str = CANCEL_EVENT_PARAM_NAME,
        menus: Optional[Dict[str, Dict]] = None,
        toolbar_actions: Optional[List[Union[ActionItem, type(Separator)]]] = None,
        window_title: Optional[str] = None,
        window_icon: Optional[str] = None,
        goto_document_start: bool = False,
        enable_progressbar: bool = False,
        progressbar_config: Optional[ProgressBarConfig] = None,
    ):
        if func_obj in self._func_bundles:
            raise AlreadyExistsError(f"function '{func_obj.__name__}' already added")

        if isinstance(widget_configs, dict):
            self._check_widget_configs(widget_configs)

        bundle = FunctionBundle(
            func_obj=func_obj,
            bind=bind,
            display_name=display_name,
            display_icon=display_icon,
            display_document=display_document,
            document_format=document_format,
            widgets_configs=widget_configs,
            cancelable=cancelable,
            cancel_event_param_name=cancel_event_param_name,
            menus=menus,
            toolbar_actions=toolbar_actions,
            window_title=window_title,
            window_icon=window_icon,
            goto_document_start=goto_document_start,
            enable_progressbar=enable_progressbar,
            progressbar_config=progressbar_config,
        )
        self._func_bundles[func_obj] = bundle

    def remove(self, func_obj: callable):
        if func_obj not in self._func_bundles:
            raise NotExistError(f"function '{func_obj.__name__}' not found")
        del self._func_bundles[func_obj]

    def get(self, func_obj: callable) -> Optional[Callable]:
        return self._func_bundles.get(func_obj, None)

    def clear(self):
        self._func_bundles.clear()

    @contextlib.contextmanager
    def instantiate_class(self, klass: Type[T]) -> T:
        try:
            if self._application is None:
                self._start_application()
            yield self._create_instance(klass=klass)
        finally:
            self._shutdown_application()

    def run(self):
        if self._application is None:
            self._start_application()
        func_count = len(self._func_bundles)
        if func_count == 0:
            msg = QApplication.tr("No functions have been added!")
            QMessageBox.warning(None, QApplication.tr("Warning"), msg)
            return
        if func_count == 1 and not self.always_show_selection_window:
            self._show_execution_window()
        else:
            self._show_selection_window()
        self._execute_application()

    def on_app_started(self, callback: Callable[[QApplication], None]):
        self._callback_app_started = callback

    def on_class_init_window_created(self, callback: Callable[[ClassInitWindow], None]):
        self._callback_class_init_window_created = callback

    def on_selection_window_created(self, callback: Callable[[SelectionWindow], None]):
        self._callback_selection_window_created = callback

    def on_execution_window_created(self, callback: Callable[[ExecutionWindow], None]):
        self._callback_execution_window_created = callback

    @property
    def class_init_window_config(self) -> ClassInitWindowConfig:
        return self._config_class_init_window

    @property
    def selection_window_config(self) -> SelectionWindowConfig:
        return self._config_selection_window

    @property
    def execution_window_config(self) -> ExecutionWindowConfig:
        return self._config_execution_window

    def _start_application(self):
        if self._application is not None:
            return
        if self._app_style:
            QApplication.setStyle(QStyleFactory.create(self._app_style))
        self._application = QApplication(self._argv)
        if self._callback_app_started is not None:
            self._callback_app_started(self._application)

    def _execute_application(self):
        if self._application is None:
            raise AppNotStartedError("application not started")
        self._application.exec()

    def _shutdown_application(self):
        if not self._application:
            return
        self._application.exit()
        self._application = None

    def _create_instance(self, klass: Type[T]) -> T:
        if not inspect.isclass(klass):
            raise TypeError(f"klass must be a class, not {type(klass)}")
        instance = ClassInitWindow.initialize_class(
            klass=klass,
            config=self._config_class_init_window,
            callback_window_created=self._callback_class_init_window_created,
            parent=None,
        )
        if instance is None:
            raise ClassInitCancelled(f"user canceled the initialization of {klass}")
        return instance

    def _show_selection_window(self):
        if self._selection_window is not None:
            self._selection_window.close()
            self._selection_window.deleteLater()
            self._selection_window = None
        self._selection_window = SelectionWindow(
            func_bundles=list(self._func_bundles.values()),
            config=self.selection_window_config,
            config_execution_window=self.execution_window_config,
            callback_window_created=self._callback_selection_window_created,
            callback_execution_window_created=self._callback_execution_window_created,
            parent=None,
        )
        self._selection_window.show()

    def _show_execution_window(self):
        if self._execution_window is not None:
            self._execution_window.close()
            self._execution_window.deleteLater()
            self._execution_window = None
        self._execution_window = ExecutionWindow(
            func_bundle=list(self._func_bundles.values())[0],
            config=self.execution_window_config,
            callback_window_created=self._callback_execution_window_created,
            parent=None,
        )
        self._execution_window.show()

    @staticmethod
    def _check_widget_configs(widget_configs: dict):
        for param_name, widget_config in widget_configs.items():
            if not isinstance(widget_config, dict):
                raise ValueError(f"'{param_name}' in widget_configs must be a dict")
            if _KEY_WIDGET_ARGS in widget_config:
                widget_args = widget_config[_KEY_WIDGET_ARGS]
                if not isinstance(widget_args, CommonParameterWidgetArgs):
                    raise ValueError(
                        f"'widget_args' must be an instance of CommonParameterWidgetArgs "
                        f"in '{param_name}''s widget_config, got {type(widget_args)}"
                    )
                if (
                    widget_args.parameter_name != param_name
                    and widget_args.parameter_name != AS_IS
                ):
                    raise ValueError("parameter_name should keep as-is")
