import threading
from concurrent.futures import Future

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QInputDialog,
    QMessageBox,
    QFileDialog,
)


class UPopup(QObject):
    request_get_text = pyqtSignal(Future, str, str, str, QLineEdit.EchoMode)
    request_get_int = pyqtSignal(Future, str, str, int, int, int, int)
    request_get_float = pyqtSignal(Future, str, str, float, float, float, int, float)
    request_get_multiline_text = pyqtSignal(Future, str, str, str)
    request_get_item = pyqtSignal(Future, list, str, str, int, bool)
    request_information = pyqtSignal(Future, str, str)
    request_warning = pyqtSignal(Future, str, str)
    request_critical = pyqtSignal(Future, str, str)
    request_question = pyqtSignal(Future, str, str)
    request_get_open_file_path = pyqtSignal(Future, str, str, str, str)
    request_get_open_file_paths = pyqtSignal(Future, str, str, str, str)
    request_get_save_file_path = pyqtSignal(Future, str, str, str, str)
    request_get_directory_path = pyqtSignal(Future, str, str)

    # noinspection PyUnresolvedReferences
    def __init__(self, window):
        super().__init__(window)
        self._window = window
        self.request_get_text.connect(self._on_get_text)
        self.request_get_int.connect(self._on_get_int)
        self.request_get_float.connect(self._on_get_float)
        self.request_get_multiline_text.connect(self._on_get_multiline_text)
        self.request_get_item.connect(self._on_get_item)
        self.request_information.connect(self._on_information)
        self.request_warning.connect(self._on_warning)
        self.request_critical.connect(self._on_critical)
        self.request_question.connect(self._on_question)
        self.request_get_open_file_path.connect(self._on_get_open_file_path)
        self.request_get_open_file_paths.connect(self._on_get_open_file_paths)
        self.request_get_save_file_path.connect(self._on_get_save_file_path)
        self.request_get_directory_path.connect(self._on_get_directory_path)

    def _on_get_text(
        self,
        future: Future[str | None],
        title: str | None = None,
        label: str | None = None,
        text: str | None = None,
        echo_mode: QLineEdit.EchoMode = QLineEdit.EchoMode.Normal,
    ):
        if not title:
            title = QApplication.tr("Input")
        if not label:
            label = QApplication.tr("Input")
        if not text:
            text = ""
        text, ok = QInputDialog.getText(self._window, title, label, echo_mode, text)
        if not ok:
            text = None
        future.set_result(text)

    def _on_get_int(
        self,
        future: Future[int | None],
        title: str = None,
        label: str = None,
        value: int = 0,
        min_val: int = -2147483647,
        max_val: int = 2147483647,
        step: int = 1,
    ):
        if not title:
            title = QApplication.tr("Input")
        if not label:
            label = QApplication.tr("Input")
        result, ok = QInputDialog.getInt(
            self._window, title, label, value, min_val, max_val, step
        )
        if not ok:
            result = None
        future.set_result(result)

    def _on_get_float(
        self,
        future: Future[int | None],
        title: str | None = None,
        label: str | None = None,
        value: float = 0.0,
        min_val: float = -2147483647.0,
        max_val: float = 2147483647.0,
        decimals: int = 3,
        step: float = 1,
    ):
        if not title:
            title = QApplication.tr("Input")
        if not label:
            label = QApplication.tr("Input")

        result, ok = QInputDialog.getDouble(
            self._window, title, label, value, min_val, max_val, decimals, step=step
        )
        if not ok:
            result = None
        future.set_result(result)

    def _on_get_multiline_text(
        self,
        future: Future[str | None],
        title: str | None = None,
        label: str | None = None,
        text: str | None = None,
    ):
        if not title:
            title = QApplication.tr("Input")
        if not label:
            label = QApplication.tr("Input")
        if not text:
            text = ""

        result, ok = QInputDialog.getMultiLineText(self._window, title, label, text)
        if not ok:
            result = None
        future.set_result(result)

    def _on_get_item(
        self,
        future: Future[str | None],
        items: list[str],
        title: str | None = None,
        label: str | None = None,
        current: int = 0,
        editable: bool = False,
    ):
        if not title:
            title = QApplication.tr("Select Item")
        if not label:
            label = QApplication.tr("Select Item")
        result, ok = QInputDialog.getItem(
            self._window, title, label, items, current, editable
        )
        if not ok:
            result = None
        future.set_result(result)

    def _on_information(self, future: Future, message: str, title: str | None = None):
        if not title:
            title = QApplication.tr("Information")
        QMessageBox.information(self._window, title, message)
        future.set_result(None)

    def _on_warning(self, future: Future, message: str, title: str | None = None):
        if not title:
            title = QApplication.tr("Warning")
        QMessageBox.warning(self._window, title, message)
        future.set_result(None)

    def _on_critical(self, future: Future, message: str, title: str | None = None):
        if not title:
            title = QApplication.tr("Critical")
        QMessageBox.critical(self._window, title, message)
        future.set_result(None)

    def _on_question(
        self, future: Future[bool], message: str, title: str | None = None
    ):
        if not title:
            title = QApplication.tr("Question")
        result = QMessageBox.question(
            self._window,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        future.set_result(result == QMessageBox.StandardButton.Yes)

    def _on_get_open_file_path(
        self,
        future: Future[str | None],
        title: str = None,
        directory: str = None,
        filters: str = None,
        init_filter: str = None,
    ):
        path, _ = QFileDialog.getOpenFileName(
            self._window, title, directory, filters, init_filter
        )
        if not path:
            future.set_result(None)
        else:
            future.set_result(path)

    def _on_get_save_file_path(
        self,
        future: Future[str | None],
        title: str = None,
        directory: str = None,
        filters: str = None,
        init_filter: str = None,
    ):
        path, _ = QFileDialog.getSaveFileName(
            self._window, title, directory, filters, init_filter
        )
        if not path:
            future.set_result(None)
        else:
            future.set_result(path)

    def _on_get_open_file_paths(
        self,
        future: Future[list[str] | None],
        title: str = None,
        directory: str = None,
        filters: str = None,
        init_filter: str = None,
    ):
        paths, _ = QFileDialog.getOpenFileNames(
            self._window, title, directory, filters, init_filter
        )
        if paths is None:
            future.set_result(None)
        else:
            future.set_result(paths)

    def _on_get_directory_path(
        self, future: Future[str | None], title: str = None, directory: str = None
    ):
        paths = QFileDialog.getExistingDirectory(self._window, title, directory)
        if paths is None:
            future.set_result(None)
        else:
            future.set_result(paths)


__current_window = None


def set_current_window(window):
    global __current_window
    __current_window = window


def _popup() -> UPopup:
    # w = QApplication.activeWindow()
    # assert hasattr(w, "popup") and isinstance(w.popup, UPopup)
    # return w.popup
    # 上述算法在某些情况下会出错，所以直接使用全局变量
    # 出错的情况是连续弹出多个对话框时，不能保证当前活动窗口是具有popup属性那个窗口
    global __current_window
    return __current_window.popup


# noinspection PyUnresolvedReferences
def get_text(
    title: str = None,
    label: str = None,
    text: str = None,
    echo_mode: QLineEdit.EchoMode = QLineEdit.EchoMode.Normal,
) -> str:
    future = Future()
    _popup().request_get_text.emit(future, title, label, text, echo_mode)
    return future.result()


# noinspection PyUnresolvedReferences
def get_float(
    title: str = None,
    label: str = None,
    value: float = 0.0,
    min_val: float = -2147483647.0,
    max_val: float = 2147483647.0,
    decimals: int = 3,
    step: float = 1.0,
) -> int:
    future = Future()
    _popup().request_get_float.emit(
        future, title, label, value, min_val, max_val, decimals, step
    )
    return future.result()


# noinspection PyUnresolvedReferences
def get_int(
    title: str = None,
    label: str = None,
    value: int = 0,
    min_val: int = -2147483647,
    max_val: int = 2147483647,
    step: int = 1,
) -> int:
    future = Future()
    _popup().request_get_int.emit(future, title, label, value, min_val, max_val, step)
    return future.result()


# noinspection PyUnresolvedReferences
def get_multiline_text(
    title: str = None,
    label: str = None,
    text: str = None,
) -> str:
    future = Future()
    _popup().request_get_multiline_text.emit(future, title, label, text)
    return future.result()


# noinspection PyUnresolvedReferences
def get_item(
    items: list[str],
    title: str = None,
    label: str = None,
    current: int = 0,
    editable: bool = False,
) -> str:
    future = Future()
    _popup().request_get_item.emit(future, items, title, label, current, editable)
    return future.result()


# noinspection PyUnresolvedReferences
def information(message: str, title: str | None = None):
    future = Future()
    _popup().request_information.emit(future, message, title)
    return future.result()


# noinspection PyUnresolvedReferences
def warning(message: str, title: str | None = None):
    future = Future()
    _popup().request_warning.emit(future, message, title)
    return future.result()


# noinspection PyUnresolvedReferences
def critical(message: str, title: str | None = None):
    future = Future()
    _popup().request_critical.emit(future, message, title)
    return future.result()


# noinspection PyUnresolvedReferences
def question(message: str, title: str | None = None) -> bool:
    future = Future()
    _popup().request_question.emit(future, message, title)
    return future.result()


# noinspection PyUnresolvedReferences
def get_open_file_path(
    title: str = None,
    directory: str = None,
    filters: str = None,
    init_filter: str = None,
) -> str | None:
    future = Future()
    _popup().request_get_open_file_path.emit(
        future, title, directory, filters, init_filter
    )
    return future.result()


# noinspection PyUnresolvedReferences
def get_open_file_paths(
    title: str = None,
    directory: str = None,
    filters: str = None,
    init_filter: str = None,
) -> list[str] | None:
    future = Future()
    _popup().request_get_open_file_paths.emit(
        future, title, directory, filters, init_filter
    )
    return future.result()


# noinspection PyUnresolvedReferences
def get_save_file_path(
    title: str = None,
    directory: str = None,
    filters: str = None,
    init_filter: str = None,
) -> str | None:
    future = Future()
    _popup().request_get_save_file_path.emit(
        future, title, directory, filters, init_filter
    )
    return future.result()


# noinspection PyUnresolvedReferences
def get_directory_path(title: str = None, directory: str = None) -> str | None:
    future = Future()
    _popup().request_get_directory_path.emit(future, title, directory)
    return future.result()
