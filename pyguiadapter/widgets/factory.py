from __future__ import annotations

from typing import Dict, Type, List, Tuple

from qtpy.QtWidgets import QWidget

from ..fn import ParameterInfo
from ..paramwidget import (
    BaseParameterWidget,
    is_parameter_widget_class,
    BaseParameterWidgetConfig,
)
from ..exceptions import AlreadyRegisteredError
from .builtin import BUILTIN_WIDGETS


class ParameterWidgetRegistry(object):
    def __init__(self):
        self._registry: Dict[str, Type[BaseParameterWidget]] = {}

        self.register_all(BUILTIN_WIDGETS)

    def register(
        self,
        typ: str | Type,
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

    def register_all(self, mapping: Dict[str | Type, Type[BaseParameterWidget]]):
        for typename, widget_class in mapping.items():
            self.register(typename, widget_class)

    def unregister(self, typ: str | Type) -> Type[BaseParameterWidget] | None:
        return self._registry.pop(self._to_typename(typ), None)

    def unregister_all(self, typs: List[str | Type]):
        for typ in typs:
            self.unregister(typ)

    def is_registered(self, typ: str | Type) -> bool:
        return self._to_typename(typ) in self._registry

    def get(self, typ: str | Type) -> Type[BaseParameterWidget] | None:
        return self._registry.get(self._to_typename(typ), None)

    def find_by_widget_class_name(
        self, widget_class_name: str
    ) -> Type[BaseParameterWidget] | None:
        return next(
            (
                widget_class
                for widget_class in self._registry.values()
                if widget_class.__name__ == widget_class_name
            ),
            None,
        )

    @staticmethod
    def _to_typename(typ: str | Type) -> str:
        if isinstance(typ, str):
            if typ.strip() == "":
                raise ValueError(f"empty string")
            return typ
        elif isinstance(typ, type) or getattr(typ, "__name__", None) is not None:
            typename = typ.__name__
            if typename.strip() == "":
                raise ValueError(f"empty string")
            return typename
        else:
            raise TypeError(f"typ must be a type or typename: {typ}")


class _ParameterWidgetFactory(ParameterWidgetRegistry):
    def __init__(self):
        super().__init__()

    def create_widget(
        self,
        param_info: ParameterInfo,
        widget_config: Tuple[
            str | Type[BaseParameterWidget], dict | BaseParameterWidgetConfig
        ],
        parent: QWidget | None = None,
    ) -> BaseParameterWidget:
        pass


ParameterWidgetFactory = _ParameterWidgetFactory()
