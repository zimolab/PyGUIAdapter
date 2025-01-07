import enum
from typing import Dict, Any, List, Optional, Tuple, Union
from ._value_type import ValueType, ValidationFailedError


class ValidationResult(enum.Enum):
    Valid = 0
    MissingKeys = 1
    UnknownKeys = 2
    InvalidValue = 3


class ValidationResultWrapper(object):
    def __init__(
        self,
        result: ValidationResult,
        key: Optional[str],
        value: Any,
        value_type: Optional[ValueType],
        missing_keys: Optional[List[str]],
        unknown_keys: Optional[List[str]],
    ):
        self._result = result
        self.key = key
        self.value = value
        self.value_type = value_type
        self.missing_keys = missing_keys
        self.unknown_keys = unknown_keys

    @classmethod
    def InvalidValue(
        cls, key: str, value: Any, value_type: ValueType
    ) -> "ValidationResultWrapper":
        return cls(ValidationResult.InvalidValue, key, value, value_type, None, None)

    @classmethod
    def MissingKeys(cls, keys: List[str]):
        return cls(ValidationResult.MissingKeys, None, None, None, keys, None)

    @classmethod
    def UnknownKeys(cls, keys: List[str]):
        return cls(ValidationResult.UnknownKeys, None, None, None, None, keys)

    @classmethod
    def Valid(cls):
        return cls(ValidationResult.Valid, None, None, None, None, None)

    @property
    def result(self) -> ValidationResult:
        return self._result

    @property
    def extra_info(
        self,
    ) -> Union[Tuple[str, Any, ValueType], List[str], None]:
        if self._result == ValidationResult.Valid:
            return None
        elif self._result == ValidationResult.MissingKeys:
            return self.missing_keys
        elif self._result == ValidationResult.UnknownKeys:
            return self.unknown_keys
        elif self._result == ValidationResult.InvalidValue:
            return self.key, self.value, self.value_type
        else:
            raise ValueError("invalid validation result")


class MissingKeysError(ValidationFailedError):
    def __init__(
        self,
        msg: str = "missing keys detected",
        missing_keys: Optional[List[str]] = None,
    ):
        self.missing_keys = missing_keys
        super().__init__(msg)


class UnknownKeysError(ValidationFailedError):
    def __init__(
        self,
        msg: str = "unknown keys detected",
        unknown_keys: Optional[List[str]] = None,
    ):
        self.unknown_keys = unknown_keys
        super().__init__(msg)


class InvalidValueError(ValidationFailedError):
    def __init__(
        self,
        msg: str = "invalid value detected",
        key: Optional[str] = None,
        value: Any = None,
        value_type: Optional[ValueType] = None,
    ):
        self.key = key
        self.value = value
        self.value_type = value_type
        super().__init__(msg)


def make_default(schema: Dict[str, ValueType]) -> Dict[str, Any]:
    return {k: v.default_value for k, v in schema.items()}


def validate_object(
    schema: Dict[str, ValueType],
    obj: Dict[str, Any],
    ignore_unknown_keys: bool = False,
    ignore_missing_keys: bool = False,
) -> ValidationResultWrapper:
    if not ignore_missing_keys:
        missing_keys = missing_keys_of(schema, obj)
        if missing_keys:
            return ValidationResultWrapper.MissingKeys(missing_keys)

    if not ignore_unknown_keys:
        unknown_keys = unknown_keys_of(schema, obj)
        if unknown_keys:
            return ValidationResultWrapper.UnknownKeys(unknown_keys)

    for k, v in obj.items():
        vt = schema.get(k, None)
        if vt is None:
            continue
        if not vt.validate(v):
            return ValidationResultWrapper.InvalidValue(k, v, vt)
    return ValidationResultWrapper.Valid()


def missing_keys_of(schema: Dict[str, ValueType], obj: Dict[str, Any]) -> List[str]:
    missing_keys = []
    for k in schema:
        if k not in obj:
            missing_keys.append(k)
    return missing_keys


def unknown_keys_of(schema: Dict[str, ValueType], obj: Dict[str, Any]) -> List[str]:
    unknown_keys = []
    for k in obj.keys():
        if k not in schema:
            unknown_keys.append(k)
    return unknown_keys


def has_missing_keys(schema: Dict[str, ValueType], obj: Dict[str, Any]) -> bool:
    for k in schema:
        if k not in obj:
            return True
    return False


def has_unknown_keys(schema: Dict[str, ValueType], obj: Dict[str, Any]) -> bool:
    for k in obj.keys():
        if k not in schema:
            return True
    return False


def remove_unknown_keys(
    schema: Dict[str, ValueType], obj: Dict[str, Any], copy: bool = True
) -> Dict[str, Any]:
    if copy:
        obj = {**obj}
    unknown_keys = unknown_keys_of(schema, obj)
    if not unknown_keys:
        return obj
    for k in unknown_keys:
        del obj[k]
    return obj


def fill_missing_keys(
    schema: Dict[str, ValueType], obj: Dict[str, Any], copy: bool = True
):
    if copy:
        obj = {**obj}
    missing_keys = missing_keys_of(schema, obj)
    if not missing_keys:
        return obj
    for k in missing_keys:
        obj[k] = schema[k].default_value
    return obj
