import dataclasses
from typing import Dict, Any, Optional, Callable, Tuple, Union

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QDialog

from ._ui import IconType, get_icon
from ..itemseditor.multiobject_editor import CommonEditorConfig, ObjectItemEditor
from ..itemseditor.object_editor import ObjectEditorConfig, ObjectEditor
from ..itemseditor.schema import (
    ValueType,
    remove_unknown_keys,
    fill_missing_keys as fill_keys,
    validate_object,
    ValidationResult,
    MissingKeysError,
    UnknownKeysError,
    InvalidValueError,
)


@dataclasses.dataclass
class SchemaObjectEditorConfig(object):
    title: str = "Object Editor"
    size: Tuple[int, int] = (500, 600)
    icon: Optional[IconType] = None
    center_container_title: str = ""
    alternating_row_colors: bool = False
    show_grid: bool = True
    show_vertical_header: bool = False
    show_horizontal_header: bool = True
    key_column_header: str = "Key"
    value_column_header: str = "Value"
    key_column_selectable: bool = True
    key_column_alignment: Union[Qt.AlignmentFlag, int, None] = Qt.AlignCenter
    value_column_alignment: Union[Qt.AlignmentFlag, int, None] = Qt.AlignCenter


@dataclasses.dataclass
class SchemaObjectPanelConfig(object):
    title: str = "Object Editor"
    size: Tuple[int, int] = (500, 600)
    icon: Optional[IconType] = None
    center_container_title: str = "12345"
    key_column_alignment: Union[Qt.AlignmentFlag, int, None] = None
    value_column_alignment: Union[Qt.AlignmentFlag, int, None] = None


def normalize_schema_object(
    schema: Dict[str, ValueType],
    obj: Dict[str, Any],
    copy: bool = True,
    fill_missing_keys: bool = False,
    ignore_unknown_keys: bool = False,
) -> Dict[str, Any]:
    if copy:
        obj = {**obj}
    if fill_missing_keys:
        obj = fill_keys(schema, obj, copy=False)
    if ignore_unknown_keys:
        obj = remove_unknown_keys(schema, obj, copy=False)
    return obj


def validate_schema_object(
    schema: Dict[str, ValueType],
    obj: Dict[str, Any],
    ignore_missing_keys: bool = False,
    ignore_unknown_keys: bool = False,
):
    if not isinstance(obj, dict):
        return TypeError("obj must be a dict")

    result_wrapper = validate_object(
        schema,
        obj,
        ignore_unknown_keys=ignore_unknown_keys,
        ignore_missing_keys=ignore_missing_keys,
    )
    result = result_wrapper.result

    if result == ValidationResult.Valid:
        return
    if result == ValidationResult.MissingKeys:
        missing_keys = result_wrapper.extra_info
        raise MissingKeysError(f"missing keys: {missing_keys}", missing_keys)
    if result == ValidationResult.UnknownKeys:
        unknown_keys = result_wrapper.extra_info
        raise UnknownKeysError(f"unknown keys: {unknown_keys}", unknown_keys)
    if result == ValidationResult.InvalidValue:
        key, value, vt = result_wrapper.extra_info
        raise InvalidValueError(f"invalid value: {key}: {value}", key, value, vt)
    raise ValueError(f"unknown validation result: {result}")


def show_schema_object_editor(
    parent: Optional[QWidget],
    schema: Dict[str, ValueType],
    obj: Dict[str, Any],
    config: SchemaObjectEditorConfig = SchemaObjectEditorConfig(),
    *,
    copy: bool = True,
    normalize_object: bool = True,
    validate: bool = True,
    accept_hook: Optional[Callable[[ObjectEditor, Dict[str, Any]], bool]] = None,
    reject_hook: Optional[Callable[[ObjectEditor], bool]] = None,
) -> Tuple[Dict[str, Any], bool]:
    """
    弹出一个结构化对象编辑器

    Args:
        parent: 父窗口
        schema: 对象的Schema
        obj: 要编辑的对象
        config: 编辑器配置
        copy: 是否复制对象
        normalize_object: 是否规范化对象，规范化对象是指：删除obj中不在schema未定义的键，并且使用默认值填充缺失的键
        validate: 是否验证对象，即检查obj是否符合schema定义的格式，如果不符合则引发异常
        accept_hook: 点击编辑器`Ok`按钮后执行的钩子函数，函数签名为(editor: ObjectEditor, obj: Dict[str, Any]) -> bool，返回True则关闭编辑器，返回False则不关闭编辑器。
        reject_hook: 点击编辑器`Cancel`按钮或关闭编辑器后执行的钩子函数，函数签名为(editor: ObjectEditor) -> bool，返回True则关闭编辑器，返回False则不关闭编辑器。

    Returns:
        返回一个元组，该元组的第一个元素是编辑后的对象，第二个元素编辑器是否accepted（一般是点击`Ok`按钮）。
    """
    if copy:
        obj = {**obj}

    if normalize_object:
        obj = normalize_schema_object(schema, obj, copy=False)

    if validate:
        validate_schema_object(schema, obj)

    editor = ObjectEditor(
        parent,
        schema=schema,
        config=ObjectEditorConfig(
            window_title=config.title,
            window_size=config.size,
            center_container_title=config.center_container_title,
            ignore_unknown_columns=True,
            alternating_row_colors=config.alternating_row_colors,
            show_vertical_header=config.show_vertical_header,
            show_horizontal_header=config.show_horizontal_header,
            show_grid=config.show_grid,
            key_item_selectable=config.key_column_selectable,
            item_text_alignment=config.key_column_alignment,
            value_item_alignment=config.value_column_alignment,
            key_column_header=config.key_column_header,
            value_column_header=config.value_column_header,
        ),
        accept_hook=accept_hook,
        reject_hook=reject_hook,
    )
    if config.icon:
        icon = get_icon(config.icon)
        if icon:
            editor.setWindowIcon(icon)
    editor.set_object(obj, normalize=False, copy=False)
    ret = editor.exec_()
    if ret == QDialog.Accepted:
        return editor.get_object(), True
    else:
        return obj, False


def show_schema_object_panel(
    parent: Optional[QWidget],
    schema: Dict[str, ValueType],
    obj: Dict[str, Any],
    config: SchemaObjectPanelConfig = SchemaObjectPanelConfig(),
    *,
    copy: bool = True,
    normalize_object: bool = True,
    validate: bool = True,
    accept_hook: Optional[Callable[[ObjectEditor, Dict[str, Any]], bool]] = None,
    reject_hook: Optional[Callable[[ObjectEditor], bool]] = None,
) -> Tuple[Dict[str, Any], bool]:
    """
    弹出一个结构化对象编辑面板

    Args:
        parent: 父窗口
        schema: 对象的Schema
        obj: 要编辑的对象
        config: 编辑器配置
        copy: 是否复制对象
        normalize_object: 是否规范化对象，规范化对象是指：删除obj中不在schema未定义的键，并且使用默认值填充缺失的键
        validate: 是否验证对象，即检查obj是否符合schema定义的格式，如果不符合则引发异常
        accept_hook: 点击编辑器`Ok`按钮后执行的钩子函数，函数签名为(editor: ObjectEditor, obj: Dict[str, Any]) -> bool，返回True则关闭编辑器，返回False则不关闭编辑器。
        reject_hook: 点击编辑器`Cancel`按钮或关闭编辑器后执行的钩子函数，函数签名为(editor: ObjectEditor) -> bool，返回True则关闭编辑器，返回False则不关闭编辑器。

    Returns:
        返回一个元组，该元组的第一个元素是编辑后的对象，第二个元素编辑器是否accepted（一般是点击`Ok`按钮）。
    """
    if copy:
        obj = {**obj}

    if normalize_object:
        obj = normalize_schema_object(schema, obj, copy=False)

    if validate:
        validate_schema_object(schema, obj)

    editor = ObjectItemEditor(
        parent,
        schema=schema,
        config=CommonEditorConfig(
            item_editor_title=config.title,
            item_editor_size=config.size,
            item_editor_center_container_title=config.center_container_title,
            item_editor_key_column_alignment=config.key_column_alignment,
            item_editor_value_column_alignment=config.value_column_alignment,
        ),
        accept_hook=accept_hook,
        reject_hook=reject_hook,
    )
    if config.icon:
        icon = get_icon(config.icon)
        if icon:
            editor.setWindowIcon(icon)
    editor.set_data(obj)
    ret = editor.exec_()
    if ret == QDialog.Accepted:
        return editor.get_data(), True
    else:
        return obj, False
