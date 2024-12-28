from typing import Optional, Dict, Any, List, Sequence

from qtpy.QtWidgets import QWidget

from ._item import ObjectItemEditor
from ..commons import ValidationFailedError
from ..itemsview_base import (
    RowBasedTableViewFrameBase,
    RowBasedTableViewFrameConfig,
    ItemEditorBase,
)
from ..schema import ValueTypeBase, ValueTypeItemDelegate


class ObjectsTableViewFrame(RowBasedTableViewFrameBase):

    def __init__(
        self,
        parent: Optional[QWidget],
        object_schema: Dict[str, ValueTypeBase],
        config: Optional[RowBasedTableViewFrameConfig] = None,
    ):
        self._config = config or RowBasedTableViewFrameConfig()

        self._object_schema: Dict[str, ValueTypeBase] = object_schema.copy()
        self._item_double_clicked_handlers: Dict[int, ValueTypeBase] = {}
        self._item_clicked_handlers: Dict[int, ValueTypeBase] = {}

        super().__init__(parent, tuple(object_schema.keys()), self._config)

        self._tableview.cellDoubleClicked.connect(self._on_item_double_clicked)
        self._tableview.cellClicked.connect(self._on_item_clicked)
        self._setup_columns()

    def normalize_object(
        self, obj: Dict[str, Any], validate_values: bool, copy: bool = False
    ) -> Dict[str, Any]:
        # when copy is True, we need to make a copy of the object
        # to avoid modifying the original object
        if copy:
            obj = obj.copy()
        missing_keys = self._tableview.missing_columns(obj)
        # to make sure all required keys are present
        # we need to fill the missing keys with default values
        # the default value is defined in the respective ValueTypeBase
        if missing_keys:
            self._fill_missing_keys(obj, missing_keys)
        if validate_values:
            for key, value in obj.items():
                vt = self._object_schema[key]
                ok = vt.validate(value)
                if not ok:
                    raise ValidationFailedError(f"validation failed: '{key}': {value}")
        return obj

    def add_object(
        self,
        obj: Dict[str, Any],
        validate_values: bool = True,
        ignore_unknown_keys: bool = False,
        *args,
        **kwargs,
    ):
        self.normalize_object(obj, validate_values)
        self._tableview.append_row(
            obj, ignore_unknown_columns=ignore_unknown_keys, *args, **kwargs
        )

    def add_objects(
        self,
        objects: Sequence[Dict[str, Any]],
        validate_values: bool = True,
        ignore_unknown_keys: bool = False,
        *args,
        **kwargs,
    ):
        for obj in objects:
            self.add_object(obj, validate_values, ignore_unknown_keys, *args, **kwargs)

    def get_objects(self, *args, **kwargs) -> List[Dict[str, Any]]:
        return self._tableview.get_all_row_data(row_indices="dict", *args, **kwargs)

    def get_object(self, row: int, *args, **kwargs) -> Dict[str, Any]:
        return self._tableview.get_row_data(row, row_data_type="dict", *args, **kwargs)

    def objects_count(self) -> int:
        return self._tableview.get_row_count()

    def remove_object_at(self, row: int, *args, **kwargs) -> Dict[str, Any]:
        return self._tableview.remove_row(row, row_data_type="dict", *args, **kwargs)

    def remove_all_objects(self, *args, **kwargs) -> None:
        self._tableview.remove_all_rows(*args, **kwargs)

    def insert_object(
        self,
        row: int,
        obj: Dict[str, Any],
        validate_values: bool = True,
        ignore_unknown_keys: bool = False,
        *args,
        **kwargs,
    ):
        self.normalize_object(obj, validate_values)
        self._tableview.insert_row(
            row, obj, ignore_unknown_columns=ignore_unknown_keys, *args, **kwargs
        )

    def update_object(
        self,
        row: int,
        obj: Dict[str, Any],
        validate_values: bool = True,
        ignore_unknown_keys: bool = False,
        *args,
        **kwargs,
    ):
        if row < 0 or row >= self._tableview.get_row_count():
            raise IndexError(f"row is out of range: {row}")
        self.normalize_object(obj, validate_values)
        self._tableview.set_row_data(
            row, obj, ignore_unknown_columns=ignore_unknown_keys, *args, **kwargs
        )

    def create_add_item_editor(self) -> ItemEditorBase:
        editor = ObjectItemEditor(self, self._object_schema)
        return editor

    def create_edit_item_editor(self) -> ItemEditorBase:
        editor = ObjectItemEditor(self, self._object_schema)
        return editor

    def _setup_columns(self):
        for column_index, column_key in enumerate(self._tableview.column_header_keys):
            column_key = self._tableview.column_header_keys[column_index]
            vt = self._object_schema[column_key]
            delegate = ValueTypeItemDelegate(self, vt)
            self._tableview.setItemDelegateForColumn(column_index, delegate)
            # hook events if needed
            if vt.hook_item_double_clicked():
                self._item_double_clicked_handlers[column_index] = vt

            if vt.hook_item_clicked():
                self._item_clicked_handlers[column_index] = vt

    def _on_item_double_clicked(self, row: int, column: int):
        if not self._item_double_clicked_handlers:
            return
        vt: ValueTypeBase = self._item_double_clicked_handlers.get(column, None)
        if not vt:
            return
        item = self._tableview.item(row, column)
        data = self._tableview.get_item_data(row, column)
        vt.on_item_double_clicked(self._tableview, row, column, data, item)

    def _on_item_clicked(self, row: int, column: int):
        if not self._item_clicked_handlers:
            return
        vt: ValueTypeBase = self._item_clicked_handlers.get(column, None)
        if not vt:
            return
        item = self._tableview.item(row, column)
        data = self._tableview.get_item_data(row, column)
        vt.on_item_clicked(self._tableview, row, column, data, item)

    def _fill_missing_keys(self, obj: Dict[str, Any], missing_keys: List[str]):
        for key in missing_keys:
            vt = self._object_schema[key]
            obj[key] = vt.default_value
        return obj
