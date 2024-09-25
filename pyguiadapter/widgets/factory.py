import warnings
from typing import Dict, Type, List, Optional, Callable, Union

from .builtin import BUILTIN_WIDGETS_MAP, BUILTIN_WIDGETS_MAPPING_RULES
from ..exceptions import AlreadyRegisteredError
from ..fn import ParameterInfo
from ..paramwidget import (
    BaseParameterWidget,
    is_parameter_widget_class,
)
from ..parser import typenames


class ParameterWidgetRegistry(object):
    def __init__(self):
        self._registry: Dict[str, Type[BaseParameterWidget]] = {}

        self.register_all(BUILTIN_WIDGETS_MAP)

    def register(
        self,
        typ: Union[str, Type],
        widget_class: Type[BaseParameterWidget],
        replace: bool = False,
    ):
        typ = self._to_typename(typ)
        if not is_parameter_widget_class(widget_class):
            raise TypeError(
                f"widget_class is not a subclass of BaseParameterWidget: {widget_class}"
            )
        old_widget_class = self._registry.get(typ, None)
        if old_widget_class is not None:
            if not replace:
                raise AlreadyRegisteredError(
                    f"typename has been registered already: {typ} -> {old_widget_class}"
                )
            else:
                self._registry[typ] = widget_class
            return
        self._registry[typ] = widget_class

    def register_all(self, mapping: Dict[Union[str, Type], Type[BaseParameterWidget]]):
        for typename, widget_class in mapping.items():
            self.register(typename, widget_class)

    def unregister(self, typ: Union[str, Type]) -> Optional[Type[BaseParameterWidget]]:
        return self._registry.pop(self._to_typename(typ), None)

    def unregister_all(self, typs: List[Union[str, Type]]):
        for typ in typs:
            self.unregister(typ)

    def is_registered(self, typ: Union[str, Type]) -> bool:
        return self._to_typename(typ) in self._registry

    def find_by_typename(
        self, typ: Union[str, Type]
    ) -> Optional[Type[BaseParameterWidget]]:
        return self._registry.get(self._to_typename(typ), None)

    def find_by_widget_class_name(
        self, widget_class_name: str
    ) -> Optional[Type[BaseParameterWidget]]:
        return next(
            (
                widget_class
                for widget_class in self._registry.values()
                if widget_class.__name__ == widget_class_name
            ),
            None,
        )

    @staticmethod
    def _to_typename(typ: Union[str, Type]) -> str:
        if isinstance(typ, str):
            if typ.strip() == "":
                raise ValueError(f"typename cannot be a empty string")
            return typ
        # elif isinstance(typ, type) or getattr(typ, "__name__", None) is not None:
        #     typename = typ.__name__
        #     if typename.strip() == "":
        #         raise ValueError(f"empty string")
        #     return typename
        # else:
        #     raise TypeError(f"typ must be a type or typename: {typ}")
        typename = typenames.get_typename(typ)
        if typename is None or typename.strip():
            raise ValueError(f"unable to get typename form: {typ}")


MappingRule = Callable[[ParameterInfo], Optional[Type[BaseParameterWidget]]]


class _ParameterWidgetFactory(ParameterWidgetRegistry):
    def __init__(self):
        super().__init__()

        self._rules: List[MappingRule] = []

        for rule in BUILTIN_WIDGETS_MAPPING_RULES:
            self.add_mapping_rule(rule)

    def find_by_rule(
        self, parameter_info: ParameterInfo
    ) -> Optional[Type[BaseParameterWidget]]:
        for rule in self._rules:
            widget_class = self._do_mapping(rule, parameter_info)
            if is_parameter_widget_class(widget_class):
                return widget_class
        return None

    def has_mapping_rule(self, rule: MappingRule) -> bool:
        return rule in self._rules

    def add_mapping_rule(self, rule: MappingRule):
        if rule not in self._rules:
            self._rules.append(rule)

    def remove_mapping_rule(self, rule: MappingRule):
        if rule in self._rules:
            self._rules.remove(rule)

    def clear_mapping_rules(self):
        self._rules.clear()

    @staticmethod
    def _do_mapping(
        rule: MappingRule, parameter_info: ParameterInfo
    ) -> Optional[Type[BaseParameterWidget]]:
        try:
            return rule(parameter_info)
        except Exception as e:
            warnings.warn(f"failed to apply mapping rule '{rule.__name__}': {e}")
            return None


ParameterWidgetFactory = _ParameterWidgetFactory()
