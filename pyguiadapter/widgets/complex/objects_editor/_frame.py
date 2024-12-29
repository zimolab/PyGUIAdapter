import dataclasses
from typing import Optional, Dict, Any, List, Sequence

from qtpy.QtWidgets import QWidget

from ._item import ObjectItemEditor
from ._view import ObjectsTableView, ObjectsTableViewConfig
from ..commons import ValidationFailedError
from ..itemsview_base import (
    RowBasedTableViewFrameBase,
    RowBasedTableViewFrameConfig,
    ItemEditorBase,
)
from ..schema import ValueTypeBase


@dataclasses.dataclass
class ObjectsTableViewFrameConfig(RowBasedTableViewFrameConfig):
    tableview_config: ObjectsTableViewConfig = dataclasses.field(
        default_factory=ObjectsTableViewConfig
    )


class ObjectsTableViewFrame(RowBasedTableViewFrameBase):

    def __init__(
        self,
        parent: Optional[QWidget],
        schema: Dict[str, ValueTypeBase],
        config: ObjectsTableViewFrameConfig,
    ):
        self._config = config
        self._schema: Dict[str, ValueTypeBase] = schema.copy()

        super().__init__(parent, tuple(schema.keys()), self._config)

    def on_create_items_view(self) -> ObjectsTableView:
        if self._tableview is None:
            self._tableview = ObjectsTableView(
                self, self._column_headers, self._schema, self._config.tableview_config
            )
            self._tableview.itemSelectionChanged.connect(self._on_selection_changed)
        return self._tableview

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
                vt = self._schema[key]
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
        editor = ObjectItemEditor(self, self._schema)
        return editor

    def create_edit_item_editor(self) -> ItemEditorBase:
        editor = ObjectItemEditor(self, self._schema)
        return editor

    def _fill_missing_keys(self, obj: Dict[str, Any], missing_keys: List[str]):
        for key in missing_keys:
            vt = self._schema[key]
            obj[key] = vt.default_value
        return obj
