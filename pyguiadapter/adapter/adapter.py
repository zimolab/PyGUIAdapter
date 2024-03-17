import contextlib
import inspect
import sys
from typing import Type, TypeAlias, Callable

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

ApplicationStartedHook: TypeAlias = Callable[[QApplication], None]


class GUIAdapter:
    def __init__(
        self,
        argv: list[str] = None,
        application_started_hook: ApplicationStartedHook | None = None,
        initialization_window_config: InitializationWindowConfig | None = None,
        selection_window_config: SelectionWindowConfig | None = None,
        execution_window_config: ExecutionWindowConfig | None = None,
        always_show_selection_window: bool = True,
    ):
        if argv is None:
            argv = sys.argv

        self._argv = argv
        self._application_started_hook = application_started_hook
        self._initialization_window_config = (
            initialization_window_config or InitializationWindowConfig()
        )
        self._selection_window_config = (
            selection_window_config or SelectionWindowConfig()
        )
        self._execution_window_config = (
            execution_window_config or ExecutionWindowConfig()
        )

        self.always_show_selection_window = always_show_selection_window

        self._functions = {}
        self._application: QApplication | None = None

        self._selection_window: SelectionWindow | None = None
        self._execution_window: ExecutionWindow | None = None

    def add(
        self,
        function: callable,
        bind: T = None,
        display_name: str = None,
        display_icon: str = None,
        display_document: str = None,
        document_format: DocumentFormat = DocumentFormat.PLAIN,
        widgets_config: dict[str, dict] = None,
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
            widgets_configs=widgets_config,
        )
        self._functions[function] = bundle

    def remove(
        self,
        function: callable,
    ):
        if function not in self._functions:
            raise NotExistError(f"function '{function.__name__}' not found")
        del self._functions[function]

    def get(self, function: callable) -> FunctionBundle | None:
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
        if self._application_started_hook is not None:
            self._application_started_hook(self._application)

    def _execute_application(self):
        if self._application is None:
            raise ApplicationNotStartedError("application not started")
        self._application.exec()

    def _shutdown_application(self):
        if not self._application:
            return
        print("shutdown application")
        self._application.exit(0)
        self._application = None

    def _create_instance(self, klass: Type[T]) -> T:
        if not inspect.isclass(klass):
            raise TypeError(f"klass must be a class, not {type(klass)}")
        instance = InitializationWindow.initialize_class(
            klass=klass, window_config=self._initialization_window_config
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
            parent=None,
        )
        self._execution_window.show()
