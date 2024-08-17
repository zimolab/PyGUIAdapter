from typing import Optional, List, Tuple

from qtpy.QtWidgets import (
    QApplication,
    QWidget,
    QLayout,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QMessageBox,
)

from ...paramwidget import BaseParameterWidget


class TestContext(object):
    def __init__(
        self,
        argv: List[str] = None,
        window_title: str = None,
        window_size: Tuple[int, int] = None,
    ):
        self._application: Optional[QApplication] = None
        self._window: Optional[QWidget] = None
        self._layout: Optional[QLayout] = None

        self._scrollarea: Optional[QScrollArea] = None
        self._widget_parameters: Optional[QWidget] = None
        self._layout_parameters: Optional[QLayout] = None
        self._button_get_parameter_values: Optional[QPushButton] = None

        self._argv = argv or []
        self._window_size = window_size
        self._window_title = window_title or "Parameter Widget Example"

    def prepare(self):
        if isinstance(self._application, QApplication):
            return
        self._application = QApplication(self._argv)
        if self._window is not None:
            self._window.close()
            self._window.deleteLater()
            self._window = None
        self._window = QWidget()
        self._window.setStyleSheet("*{font-size: 12pt}")
        if self._window_size is not None:
            self._window.resize(*self._window_size)
        if self._window_title is not None:
            self._window.setWindowTitle(self._window_title)
        self._layout = QVBoxLayout(self._window)
        self._window.setLayout(self._layout)

        self._scrollarea = QScrollArea(self._window)
        self._scrollarea.setWidgetResizable(True)
        self._widget_parameters = QWidget(self._scrollarea)
        self._scrollarea.setWidget(self._widget_parameters)

        self._layout_parameters = QVBoxLayout(self._widget_parameters)
        self._widget_parameters.setLayout(self._layout_parameters)

        self._button_get_parameter_values = QPushButton(
            "Get Parameter Values", self._window
        )
        # noinspection PyUnresolvedReferences
        self._button_get_parameter_values.clicked.connect(self.get_parameter_values)

        self._layout.addWidget(self._scrollarea)
        self._layout.addWidget(self._button_get_parameter_values)

    def dispose(self):
        if self._window is not None:
            self._window.close()
            self._window.deleteLater()
            self._window = None

        if self._application is not None:
            self._application.quit()
            self._application = None

        self._layout = None
        self._layout_parameters = None
        self._widget_parameters = None
        self._button_get_parameter_values = None

    def add_widget(self, widget: BaseParameterWidget):
        widget.setParent(self._window)
        self._layout_parameters.addWidget(widget)

    def exec(self):
        self._window.show()
        self._application.exec()

    def get_parameter_values(self):
        values = {}
        # 遍历布局中的所有控件，获取其值
        for i in range(self._layout_parameters.count()):
            item = self._layout_parameters.itemAt(i)
            widget = item.widget()
            if not isinstance(widget, BaseParameterWidget):
                continue
            widget: BaseParameterWidget
            values[widget.parameter_name] = widget.get_value()
        msg = "current parameter values:\n\n"
        for key, value in values.items():
            msg += f"{key}: {value}\n"
        msg += "\n"
        QMessageBox.information(self._window, "Parameter Values", msg)

    def __enter__(self):
        self.prepare()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
