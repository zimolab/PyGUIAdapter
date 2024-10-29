"""
@Time    : 2024.10.20
@File    : _core.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 一些重要的工具函数和类型定义
"""

import ast
import base64
import hashlib
import inspect
import re
import traceback
import warnings
from fnmatch import fnmatch, fnmatchcase
from io import StringIO
from typing import List, Set, Tuple, Any, Union, Optional, Type

PyLiteralType = Union[bool, int, float, bytes, str, list, tuple, dict, set, type(None)]


def _marks(marks: Union[str, List[str], Tuple[str], Set[str]]) -> Set[str]:
    if not isinstance(marks, (list, tuple, set, str)):
        raise TypeError(f"unsupported types for marks: {type(marks)}")
    if isinstance(marks, str):
        if marks.strip() == "":
            raise ValueError("marks must be a non-empty string")
        return {marks}

    if len(marks) <= 0:
        raise ValueError("at least one mark must be provided")

    tmp = set()
    for mark in marks:
        if not isinstance(mark, str):
            raise TypeError(f"a mark must be a string: {type(mark)}")
        if mark.strip() == "":
            raise ValueError("an empty-string mark found")
        tmp.add(mark)
    return tmp


def _block_pattern(
    start_marks: Union[str, List[str], Tuple[str], Set[str]],
    end_marks: Union[str, List[str], Tuple[str], Set[str]],
) -> str:
    start_marks = _marks(start_marks)
    end_marks = _marks(end_marks)

    start_mark_choices = "|".join(start_marks)
    end_mark_choices = "|".join(end_marks)
    pattern = (
        rf"^(\s*(?:{start_mark_choices})\s*(.*\n.+)^\s*(?:{end_mark_choices})\s*\n)"
    )
    return pattern


def extract_text_block(
    text: str,
    start_marks: Union[str, List[str], Tuple[str], Set[str]],
    end_marks: Union[str, List[str], Tuple[str], Set[str]],
) -> Optional[str]:
    pattern = _block_pattern(start_marks, end_marks)
    result = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.UNICODE)
    if result:
        return result.group(2)
    return None


def remove_text_block(
    text: str,
    start_marks: Union[str, List[str], Tuple[str], Set[str]],
    end_marks: Union[str, List[str], Tuple[str], Set[str]],
) -> str:
    pattern = _block_pattern(start_marks, end_marks)
    result = re.search(pattern, text, re.MULTILINE | re.DOTALL | re.UNICODE)
    if not result:
        return text
    return re.sub(
        pattern, repl="", string=text, flags=re.MULTILINE | re.DOTALL | re.UNICODE
    )


def hashable(obj: Any) -> bool:
    try:
        hash(obj)
        return True
    except TypeError:
        return False


def unique_list(origin: List[Any]) -> List[Any]:
    added = set()
    bool_true_added = False
    bool_false_added = False
    ret = []
    for item in origin:
        if item is True:
            if not bool_true_added:
                ret.append(item)
                bool_true_added = True
        elif item is False:
            if not bool_false_added:
                ret.append(item)
                bool_false_added = True
        else:
            if item not in added:
                added.add(item)
                ret.append(item)
    return ret


def fingerprint(text: str) -> Optional[str]:
    if not text:
        return None
    md5 = hashlib.md5()
    md5.update(text.encode("utf-8"))
    return md5.hexdigest()


def get_object_filename(obj: Any) -> Optional[str]:
    return inspect.getsourcefile(obj)


def get_object_sourcecode(obj: Any) -> Optional[str]:
    return inspect.getsource(obj)


def get_type_args(raw: str) -> list:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        content = raw[1:-1].strip()
    elif raw.startswith("(") and raw.endswith(")"):
        content = raw[1:-1].strip()
    else:
        content = None

    if content is None:
        return raw.split(",")

    content = "[" + content + "]"
    try:
        args = ast.literal_eval(content)
    except Exception as e:
        warnings.warn(f"unable to parse type args '{raw}': {e}")
        return []
    return args


def is_subclass_of(cls: Any, base_cls: Any):
    if not inspect.isclass(cls) or not inspect.isclass(base_cls):
        return False
    return issubclass(cls, base_cls)


def get_traceback(
    error: Exception, limit: Optional[int] = None, complete_msg: bool = True
) -> str:
    assert isinstance(error, Exception)
    buffer = StringIO()
    if complete_msg:
        buffer.write("Traceback (most recent call last):\n")
    traceback.print_tb(error.__traceback__, limit=limit, file=buffer)
    if complete_msg:
        buffer.write(f"{type(error).__name__}: {error}")
    msg = buffer.getvalue()
    buffer.close()
    return msg


def type_check(value: Any, allowed_types: Tuple[Type[Any], ...], allow_none: bool):
    if allow_none and value is None:
        return
    if not isinstance(value, allowed_types):
        raise TypeError(f"invalid type: {type(value)}")


def to_base64(data: Union[bytes, str]) -> str:
    return base64.b64encode(data).decode()


def get_file_filter_pattern(filter_str: str) -> Optional[str]:
    p = r"^.*\s*\(\s*([\w\W]+)\s*\)\s*$"
    match = re.match(p, filter_str)
    if not match:
        return None
    return match.group(1).strip()


def match_file_filters(
    filters: str, file_path: str, case_sensitive: bool = False
) -> Tuple[bool, Optional[str]]:
    filters = [
        get_file_filter_pattern(f)
        for f in filters.strip().split(";")
        if f.strip() != ""
    ]

    matched = False
    filter_pattern = None
    for filter_pattern in filters:
        if not filter_pattern:
            continue

        if not case_sensitive:
            matched = fnmatch(file_path, filter_pattern)
            if matched:
                break
        else:
            matched = fnmatchcase(file_path, filter_pattern)
            if matched:
                break
    if not matched:
        return False, None
    return True, filter_pattern
