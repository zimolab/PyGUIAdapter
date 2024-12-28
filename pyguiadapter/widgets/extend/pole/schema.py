from typing import Dict, Union, Any, Callable

from .valuetypes import StringValue, IntValue, ValueTypeBase, FilePathValue
from ...builtin import TYPE_INT, TYPE_STR, TYPE_FILE_T
from ....parser.typenames import get_typename

_DEFAULT_STRING_VALUE_TYPE = StringValue()

_DEFAULT_VALUE_TYPE_MAP = {
    TYPE_INT: IntValue(),
    TYPE_STR: _DEFAULT_STRING_VALUE_TYPE,
    TYPE_FILE_T: FilePathValue(),
}


def _to_typename(typ: Any) -> str:
    if isinstance(typ, str):
        if typ.strip() == "":
            raise ValueError(f"typename cannot be a empty string")
        return typ
    typename = get_typename(typ)
    if typename is None or typename.strip() == "":
        raise ValueError(f"unable to get typename form: {typ}")
    return typename


def normalize_object_schema(
    schema: Dict[str, Union[ValueTypeBase, type, str, None]]
) -> Dict[str, ValueTypeBase]:
    norm = {}
    for key, value_type in schema.items():
        if isinstance(value_type, ValueTypeBase):
            norm[key] = value_type
        elif value_type is None:
            norm[key] = _DEFAULT_STRING_VALUE_TYPE
        else:
            value_type = _DEFAULT_VALUE_TYPE_MAP.get(_to_typename(value_type), None)
            if value_type is None:
                raise ValueError(f"unknown value type: {value_type}")
            norm[key] = value_type
    return norm


def unknown_to_string_value_type(key: str, value: Any) -> ValueTypeBase:
    _ = key, value  # unused
    return _DEFAULT_STRING_VALUE_TYPE


def raise_on_unknown(key: str, value: Any) -> None:
    _ = key, value  # unused
    raise ValueError(f"cannot infer value type for {key}: {value}")


def infer_from_example(
    obj: Dict[str, Any],
    when_not_inferred: Callable[[str, Any], ValueTypeBase] = raise_on_unknown,
) -> Dict[str, ValueTypeBase]:
    schema = {}
    for key, value in obj.items():
        typ = type(value)
        value_type = _DEFAULT_VALUE_TYPE_MAP.get(_to_typename(typ), None)
        if value_type is None:
            value_type = when_not_inferred(key, value)
        schema[key] = value_type
    return schema
