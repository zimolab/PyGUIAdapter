import contextlib
import inspect
import sys
from typing import Type, Callable, Optional, List, Dict

from PyQt6.QtWidgets import QApplication, QMessageBox

from pyguiadapter.adapter.bundle import FunctionBundle
from pyguiadapter.commons import T, DocumentFormat
from pyguiadapter.exceptions import (
    AlreadyExistsError,
    NotExistError,
    ApplicationNotStartedError,
    InitializationCancelled,
)
from pyguiadapter.ui.window.execution import ExecutionWindowConfig, ExecutionWindow
from pyguiadapter.ui.window.initialization import (
    InitializationWindow,
    InitializationWindowConfig,
)
from pyguiadapter.ui.window.selection import SelectionWindowConfig, SelectionWindow

ALWAYS_SHOW_SELECTION_WINDOW: bool = False


class GUIAdapter:
    def __init__(
        self,
        argv: List[str] = None,
        *,
        initialization_window_config: Optional[InitializationWindowConfig] = None,
        selection_window_config: Optional[SelectionWindowConfig] = None,
        execution_window_config: Optional[ExecutionWindowConfig] = None,
        application_started_callback: Optional[Callable[[QApplication], None]] = None,
        always_show_selection_window: bool = ALWAYS_SHOW_SELECTION_WINDOW,
        initialization_window_created_callback: Optional[
            Callable[[InitializationWindow], None]
        ] = None,
        selection_window_created_callback: Optional[
            Callable[[SelectionWindow], None]
        ] = None,
        execution_window_created_callback: Optional[
            Callable[[ExecutionWindow], None]
        ] = None,
    ):
        if argv is None:
            argv = sys.argv

        self._argv = argv
        self._initialization_window_config = (
            initialization_window_config or InitializationWindowConfig()
        )
        self._selection_window_config = (
            selection_window_config or SelectionWindowConfig()
        )
        self._execution_window_config = (
            execution_window_config or ExecutionWindowConfig()
        )

        self._application_started_callback = application_started_callback
        self._execution_window_created_callback = execution_window_created_callback
        self._initialization_window_created_callback = (
            initialization_window_created_callback
        )
        self._selection_window_created_callback = selection_window_created_callback

        self.always_show_selection_window = always_show_selection_window

        self._functions = {}
        self._application: Optional[QApplication] = None

        self._selection_window: Optional[SelectionWindow] = None
        self._execution_window: Optional[ExecutionWindow] = None

    def add(
        self,
        function: callable,
        bind: T = None,
        display_name: str = None,
        display_icon: str = None,
        display_document: str = None,
        document_format: DocumentFormat = DocumentFormat.PLAIN,
        widget_configs: Dict[str, dict] = None,
    ):
        if function in self._functions:
            raise AlreadyExistsError(f"function '{function.__name__}' already added")
        bundle = FunctionBundle(
            function=function,
            bind=bind,
            display_name=display_name,
            display_icon=display_icon,
            display_document=display_document,
            document_format=document_format,
            widgets_configs=widget_configs,
        )
        self._functions[function] = bundle

    def remove(self, function: callable):
        if function not in self._functions:
            raise NotExistError(f"function '{function.__name__}' not found")
        del self._functions[function]

    def get(self, function: callable) -> Optional[FunctionBundle]:
        return self._functions.get(function, None)

    def clear(self):
        self._functions.clear()

    @contextlib.contextmanager
    def initialize_class(self, klass: Type[T]) -> T:
        try:
            if self._application is None:
                self._start_application()
            yield self._create_instance(klass=klass)
        finally:
            self._shutdown_application()

    def run(self):
        if self._application is None:
            self._start_application()
        function_count = len(self._functions)
        if function_count == 0:
            msg = QApplication.tr("No functions have been added!")
            QMessageBox.warning(None, QApplication.tr("Warning"), msg)
            return
        if function_count == 1 and not self.always_show_selection_window:
            self._show_execution_window()
        else:
            self._show_selection_window()
        self._execute_application()

    def on_application_started(self, callback: Callable[[QApplication], None]):
        self._application_started_callback = callback

    def on_initialization_window_created(
        self, callback: Callable[[InitializationWindow], None]
    ):
        self._initialization_window_created_callback = callback

    def on_selection_window_created(self, callback: Callable[[SelectionWindow], None]):
        self._selection_window_created_callback = callback

    def on_execution_window_created(self, callback: Callable[[ExecutionWindow], None]):
        self._execution_window_created_callback = callback

    @property
    def initialization_window_config(self) -> InitializationWindowConfig:
        return self._initialization_window_config

    @property
    def selection_window_config(self) -> SelectionWindowConfig:
        return self._selection_window_config

    @property
    def execution_window_config(self) -> ExecutionWindowConfig:
        return self._execution_window_config

    def _start_application(self):
        if self._application is not None:
            return
        self._application = QApplication(self._argv)
        if self._application_started_callback is not None:
            self._application_started_callback(self._application)

    def _execute_application(self):
        if self._application is None:
            raise ApplicationNotStartedError("application not started")
        self._application.exec()

    def _shutdown_application(self):
        if not self._application:
            return
        self._application.exit()
        self._application = None

    def _create_instance(self, klass: Type[T]) -> T:
        if not inspect.isclass(klass):
            raise TypeError(f"klass must be a class, not {type(klass)}")
        instance = InitializationWindow.initialize_class(
            klass=klass,
            window_config=self._initialization_window_config,
            window_created_callback=self._initialization_window_created_callback,
            parent=None,
        )
        if instance is None:
            raise InitializationCancelled(
                f"user canceled the initialization of {klass}"
            )
        return instance

    def _show_selection_window(self):
        if self._selection_window is not None:
            self._selection_window.close()
            self._selection_window.deleteLater()
            self._selection_window = None
        self._selection_window = SelectionWindow(
            functions=list(self._functions.values()),
            window_config=self.selection_window_config,
            execution_window_config=self.execution_window_config,
            window_created_callback=self._selection_window_created_callback,
            execution_window_created_callback=self._execution_window_created_callback,
            parent=None,
        )
        self._selection_window.show()

    def _show_execution_window(self):
        if self._execution_window is not None:
            self._execution_window.close()
            self._execution_window.deleteLater()
            self._execution_window = None
        self._execution_window = ExecutionWindow(
            function=list(self._functions.values())[0],
            window_config=self.execution_window_config,
            created_callback=self._execution_window_created_callback,
            parent=None,
        )
        self._execution_window.show()
