from typing import Optional, Any, Union

from qtpy.QtWidgets import (
    QLineEdit,
    QToolButton,
    QFileDialog,
    QWidget,
    QHBoxLayout,
    QTableWidgetItem,
)

from .._commons import KEY_COLUMN_INDEX
from ..object_edit import ObjectEditView
from ..schema import ValueWidgetMixin, ValueType, CellWidgetMixin


class PathSelector(QFileDialog, ValueWidgetMixin):

    def __init__(self, parent: Optional[QWidget], default_value: str):
        super().__init__(parent)
        self.setModal(True)
        self.setFileMode(QFileDialog.Directory)
        # self.setDirectory(default_value)
        self.setOption(QFileDialog.ShowDirsOnly, True)

        self._default_value = default_value
        self._accepted = False

    def set_value(self, value: str):
        self._default_value = value
        self._accepted = False

    def get_value(self) -> Any:
        selected = self.selectedFiles()
        if selected and self._accepted:
            return selected[0]
        else:
            return self._default_value

    def accept(self):
        self._accepted = True
        super().accept()


class PathEdit(QWidget, CellWidgetMixin):
    def __init__(self, parent: Optional[QWidget], default_value: str):
        super().__init__(parent)
        self._default_value = default_value
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._line_edit = QLineEdit(self)
        self._line_edit.setText(default_value)
        self._layout.addWidget(self._line_edit)

        self._browse_button = QToolButton(self)
        self._browse_button.setText("...")
        self._browse_button.clicked.connect(self._on_browse_button_clicked)
        self._layout.addWidget(self._browse_button)

        self.setLayout(self._layout)

    def _on_browse_button_clicked(self):
        dialog = PathSelector(self, self._default_value)
        ret = dialog.exec_()
        if ret != QFileDialog.Accepted:
            return
        path = dialog.get_value()
        self._line_edit.setText(path)
        dialog.deleteLater()

    def get_value(self) -> str:
        return self._line_edit.text()

    def set_value(self, value: str):
        self._line_edit.setText(value)


class PathValue(ValueType):

    def __init__(self, default_value: str = ""):
        super().__init__(default_value)

    def validate(self, value: Any) -> bool:
        return isinstance(value, str)

    def create_item_editor_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin, None]:
        return PathEdit(parent, self.default_value)

    def create_item_delegate_widget(
        self, parent: QWidget, *args, **kwargs
    ) -> Union[QWidget, ValueWidgetMixin]:
        return PathSelector(parent, self.default_value)

    def after_set_item_data(
        self, row: int, col: int, item: QTableWidgetItem, value: Any
    ):
        if item:
            if (
                isinstance(item.tableWidget(), ObjectEditView)
                and col == KEY_COLUMN_INDEX
            ):
                # this is a special case for object editor,
                # we don't want to show tooltip for key column
                return
            text = str(value)
            item.setToolTip(text)
