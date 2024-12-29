from typing import Dict, Union, Any

from ._value_type import ValueType
from ...exceptions import AlreadyExistError, NotFoundError


class ObjectSchemaFactory(object):
    def __init__(self):
        self._registry: Dict[type, ValueType] = {}

    def register(self, typ: type, vt: ValueType):
        if not isinstance(typ, type):
            raise TypeError(f"typ must be a type, got {type(typ)}")

        if not isinstance(vt, ValueType):
            raise TypeError(f"vt must be a ValueTypeBase, got {vt}")

        if typ in self._registry:
            raise AlreadyExistError(f"type '{typ}' already registered")

        self._registry[typ] = vt

    def unregister(self, typ: type) -> ValueType:
        if not typ in self._registry:
            raise NotFoundError(f"type '{typ}' not registered yet")
        return self._registry.pop(typ)

    def clear(self):
        self._registry.clear()

    def get_value_type(self, typ: type) -> ValueType:
        if not typ in self._registry:
            raise NotFoundError(f"type '{typ}' not registered yet")
        return self._registry[typ]

    def create_schema(
        self, schema_dict: Dict[str, Union[ValueType, type, str, Any]]
    ) -> Dict[str, ValueType]:
        schema = {}
        for key, type_or_value in schema_dict.items():
            if isinstance(type_or_value, ValueType):
                schema[key] = type_or_value
                continue
            # if it's a type, get the value type from the registry
            if isinstance(type_or_value, type):
                vt = self.get_value_type(type_or_value)
                schema[key] = vt
                continue

            # if it is not a ValueTypeBase or a type, assume it's a default value of a ValueTypeBase
            # so we need to get the corresponding ValueTypeBase from the registry (if registered)
            # and create a new instance with the default value
            typ = type(type_or_value)
            default_vt = self.get_value_type(typ)
            vt_class = default_vt.__class__
            new_vt = vt_class(default_value=type_or_value)
            schema[key] = new_vt

        return schema
