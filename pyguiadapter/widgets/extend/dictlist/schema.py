import dataclasses
from abc import abstractmethod

from typing import Any, Optional, Dict, Tuple, List

from qtpy.QtCore import QModelIndex, Qt, QAbstractItemModel, QDateTime
from qtpy.QtWidgets import (
    QWidget,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QDialog,
    QApplication,
    QAbstractItemView,
    QTableWidgetItem,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QDateTimeEdit,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QLabel,
)

from pyguiadapter.widgets.extend.pathlist2.itemdlg import PathItemEditor


class DictValueWidgetInterface(QWidget):

    @abstractmethod
    def set_value(self, value: Any):
        pass

    @abstractmethod
    def get_value(self) -> Any:
        pass


class BaseDictValue(object):

    @abstractmethod
    def create_widget(self, parent: QWidget) -> DictValueWidgetInterface:
        pass


class IntValueWidget(DictValueWidgetInterface):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._spinbox = QSpinBox(self)
        self._layout.addWidget(self._spinbox)

    def set_value(self, value: int):
        self._spinbox.setValue(value)

    def get_value(self) -> int:
        return self._spinbox.value()


class IntValue(BaseDictValue):

    def create_widget(self, parent: QWidget) -> DictValueWidgetInterface:
        return IntValueWidget(parent)


class DateTimeValueWidget(DictValueWidgetInterface):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._date_edit = QDateTimeEdit(self)
        self._layout.addWidget(self._date_edit)

    def set_value(self, value: QDateTime):
        self._date_edit.setDateTime(value)

    def get_value(self) -> QDateTime:
        return self._date_edit.dateTime()


class DateTimeValue(BaseDictValue):

    def create_widget(self, parent: QWidget) -> DictValueWidgetInterface:
        return DateTimeValueWidget(parent)


class FilePathValueWidget(QPushButton, DictValueWidgetInterface):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._current_value = ""
        # self._layout = QHBoxLayout()
        # self._layout.setContentsMargins(0, 0, 0, 0)
        # # self._layout.setSpacing(0)
        # self.setLayout(self._layout)
        #
        # self._file_edit = QLineEdit(self)
        # self._layout.addWidget(self._file_edit)
        #
        # self._browser_file_button = QPushButton("Browse", self)
        # self._browser_file_button.clicked.connect(self._on_browse_file)
        # self._layout.addWidget(self._browser_file_button)
        self._current_value = ""
        self.setText("Browse File")
        self.clicked.connect(self._on_browse_file)

    def set_value(self, value: str):
        self._current_value = value

    def get_value(self) -> str:
        return self._current_value

    def _on_browse_file(self):
        edt = PathItemEditor(self)
        edt.current_value = self._current_value
        ret = edt.exec()
        if ret == QDialog.Accepted:
            self._current_value = edt.current_value
        edt.destroy()
        edt.deleteLater()
        self.parentWidget().setFocus()

    # def _on_accept(self):
    #     self.setText(self._editor.current_value)


class FilePathValue(BaseDictValue):
    def create_widget(self, parent: QWidget) -> DictValueWidgetInterface:
        return FilePathValueWidget(parent)


_DEFAULT_SIZE = (600, 400)


class DictValueWidgetDelegate(QStyledItemDelegate):
    def __init__(self, parent: QWidget, value_def: BaseDictValue):
        super().__init__(parent)
        self._value_def = value_def

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> Optional[QWidget]:
        if not index.isValid():
            return None
        value_widget = self._value_def.create_widget(parent)
        return value_widget

    def setEditorData(
        self, value_widget: DictValueWidgetInterface, index: QModelIndex
    ) -> None:
        data = index.data(Qt.EditRole)
        if data is None:
            return
        value_widget.set_value(data)

    def setModelData(
        self,
        value_widget: DictValueWidgetInterface,
        model: QAbstractItemModel,
        index: QModelIndex,
    ) -> None:
        model.setData(index, value_widget.get_value(), Qt.EditRole)

    def destroyEditor(
        self, value_widget: DictValueWidgetInterface, index: QModelIndex
    ) -> None:
        super().destroyEditor(value_widget, index)


@dataclasses.dataclass
class DictListEditConfig(object):
    dict_schema: Dict[str, BaseDictValue] = dataclasses.field(default_factory=dict)
    editor_title: str = ""
    editor_size: Optional[Tuple[int, int]] = None


class DictListEditor(QDialog):
    def __init__(self, config: DictListEditConfig, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._config = config

        if not self._config.dict_schema:
            raise ValueError("dict_schema cannot be empty")

        self._key_to_col = {}

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._table_widget = QTableWidget(self)
        self._setup_table_widget()
        self._layout.addWidget(self._table_widget)

        self.resize(*self._config.editor_size or _DEFAULT_SIZE)

    def add_item(self, item: Dict[str, Any], ignore_unknown_keys: bool = False):
        row = self._table_widget.rowCount()
        self._table_widget.insertRow(row)
        for key in item:
            value = item[key]
            col = self._col_for_key(key)
            if col == -1:
                if ignore_unknown_keys:
                    continue
                else:
                    raise ValueError(f"unknown key: {key}")
            col_item = QTableWidgetItem()
            col_item.setData(Qt.EditRole, value)
            self._table_widget.setItem(row, col, col_item)

    @property
    def items(self) -> List[Dict[str, Any]]:
        ret = []
        for row in range(self._table_widget.rowCount()):
            ret.append(self._get_item_at(row))
        return ret

    def _get_item_at(self, row: int) -> Dict[str, Any]:
        item = {}
        for col in range(self._table_widget.columnCount()):
            key = self._table_widget.horizontalHeaderItem(col).text()
            value = self._table_widget.item(row, col).data(Qt.EditRole)
            item[key] = value
        return item

    def _col_for_key(self, key: str) -> int:
        return self._key_to_col.get(key, -1)

    def _setup_table_widget(self):
        headers = list(self._config.dict_schema.keys())
        self._table_widget.setColumnCount(len(headers))
        self._key_to_col = {k: i for i, k in enumerate(headers)}
        self._table_widget.setHorizontalHeaderLabels(headers)
        self._table_widget.horizontalHeader().setStretchLastSection(True)
        self._table_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self._table_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        for key, col in self._key_to_col.items():
            value_def = self._config.dict_schema.get(key, None)

            if value_def is None:
                continue
            delegate = DictValueWidgetDelegate(self, value_def)
            self._table_widget.setItemDelegateForColumn(col, delegate)


if __name__ == "__main__":
    app = QApplication([])

    config = DictListEditConfig(
        dict_schema={
            "name": None,
            "age": IntValue(),
            "gender": IntValue(),
            "birthday": DateTimeValue(),
            "profile": FilePathValue(),
        }
    )
    editor = DictListEditor(config)
    editor.add_item(
        {
            "name": "Alice",
            "age": 25,
            "gender": 1,
            "birthday": QDateTime().currentDateTime(),
            "profile": "/path/to/profile.jpg",
        }
    )
    editor.show()
    app.exec_()
    print(editor.items)
