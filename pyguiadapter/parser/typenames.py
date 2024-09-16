import re
from collections.abc import Mapping, MutableMapping, MutableSet, Set
from collections import OrderedDict
import typing

from .. import utils

TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_STR = "str"
TYPE_BOOL = "bool"
TYPE_DICT = "dict"
TYPE_LIST = "list"
TYPE_SET = "set"
TYPE_TUPLE = "tuple"
TYPE_ANY = "any"
TYPE_ORDERED_DICT = "OrderedDict"
TYPE_LITERAL = "literal"

_TYPE_ANN_PATTERN = r"(\w+)\[\s*([\w\W]+)\s*\]"

BasicTypeMap = {
    int: TYPE_INT,
    float: TYPE_FLOAT,
    str: TYPE_STR,
    bool: TYPE_BOOL,
    dict: TYPE_DICT,
    list: TYPE_LIST,
    set: TYPE_SET,
    tuple: TYPE_TUPLE,
    object: TYPE_ANY,
    any: TYPE_ANY,
    Mapping: TYPE_DICT,
    MutableMapping: TYPE_DICT,
    MutableSet: TYPE_SET,
    Set: TYPE_SET,
    OrderedDict: TYPE_ORDERED_DICT,
    typing.Any: TYPE_ANY,
    typing.TypedDict: TYPE_DICT,
    typing.Literal: TYPE_LITERAL,
    typing.Union: TYPE_ANY,
    typing.Optional: TYPE_ANY,
}

ExtendTypeMap = {
    typing.TypedDict: TYPE_DICT,
    typing.Union: TYPE_ANY,
    typing.Optional: TYPE_ANY,
}


def _get_typename_from_str_annotation(typ: str) -> str:
    match = re.match(_TYPE_ANN_PATTERN, typ)
    if match is not None:
        return match.group(1)
    return typ


def _get_type_args_from_str_annotation(typ: str) -> typing.List[str]:
    match = re.match(_TYPE_ANN_PATTERN, typ)
    if match is not None:
        type_arg_str = match.group(2)
        return utils.get_type_args(type_arg_str.strip())
    return []


def _get_extend_typename(typ: typing.Any) -> str:
    if isinstance(typ, type) or getattr(typ, "__name__", None) is not None:
        return typ.__name__
    return type(typ).__name__


def get_typename(typ: typing.Any) -> str:
    if isinstance(typ, str):
        typ = typ.strip()
        return _get_typename_from_str_annotation(typ)

    if not utils.hashable(typ):
        return _get_extend_typename(typ)

    typename = BasicTypeMap.get(typ, None)
    if typename is not None:
        return typename

    origin_typ = typing.get_origin(typ)

    typename = BasicTypeMap.get(origin_typ, None)
    if typename is not None:
        return typename

    typename = ExtendTypeMap.get(origin_typ, None)
    if typename is not None:
        return typename
    return _get_extend_typename(typ)


def get_type_args(typ: typing.Any) -> typing.List[typing.Any]:
    if isinstance(typ, str):
        typ = typ.strip()
        return _get_type_args_from_str_annotation(typ)
    args = []
    for arg in typing.get_args(typ):
        if isinstance(arg, (int, float, str, bool, dict, list, set, tuple)):
            args.append(arg)
        else:
            args.append(get_typename(arg))
    return args
