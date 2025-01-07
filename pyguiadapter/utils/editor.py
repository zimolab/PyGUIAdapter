from typing import Dict, Any

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


# def show_object_editor(
#     arent: Optional[QWidget],
#     schema: Dict[str, ValueType],
#     obj: Dict[str, Any],
#     config: ObjectEditorConfig,
#     *,
#     copy: bool = True,
#     validate_object: bool = True,
#     normalize_object: bool = True,
#     accept_hook: Optional[Callable[[ObjectEditor, Dict[str, Any]], bool]] = None,
#     reject_hook: Optional[Callable[[ObjectEditor], bool]] = None,
# ) -> Tuple[Dict[str, Any], bool]:
#     if copy:
#         obj = {**obj}
#
#     if normalize_object:
#         fill_keys(schema, obj, copy=False)
#         remove_unknown_keys(schema, obj, copy=False)
#
#     if validate_object:
#         pass
