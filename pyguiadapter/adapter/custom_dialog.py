from __future__ import annotations

import inspect
from abc import abstractmethod
from typing import Type, Any

from qtpy.QtWidgets import QWidget, QDialog

from ..exceptions import AlreadyRegisteredError, NotRegisteredError


class BaseCustomDialog(QDialog):
    def __init__(self, parent: QWidget | None, **kwargs):
        super().__init__(parent)

    @abstractmethod
    def get_result(self) -> Any:
        pass


class CustomDialogFactory(object):
    def __init__(self):
        self._dialog_classes = {}

    def register(
        self, dialog_class: Type[BaseCustomDialog], name: str | None = None
    ) -> str:
        if not (
            inspect.isclass(dialog_class) and issubclass(dialog_class, BaseCustomDialog)
        ):
            raise TypeError(
                f"dialog_class must be a subclass of BaseCustomDialog: {dialog_class}"
            )
        if not name:
            name = dialog_class.__name__
        if name in self._dialog_classes:
            raise AlreadyRegisteredError(f"name already registered: {name}")
        self._dialog_classes[name] = dialog_class
        return name

    def unregister(
        self, class_or_name: str | Type[BaseCustomDialog]
    ) -> Type[BaseCustomDialog] | None:
        if not isinstance(class_or_name, str):
            class_or_name = class_or_name.__name__
        if class_or_name not in self._dialog_classes:
            return None
        return self._dialog_classes.pop(class_or_name)

    def clear(self):
        self._dialog_classes.clear()

    def get(self, name: str) -> Type[BaseCustomDialog] | None:
        return self._dialog_classes.get(name, None)

    def create(
        self, parent: QWidget, dialog_class: str | Type[BaseCustomDialog], **kwargs
    ) -> BaseCustomDialog:
        if isinstance(dialog_class, str):
            dialog_class = self.get(dialog_class)
        if not dialog_class:
            raise NotRegisteredError(f"dialog class not registered: {dialog_class}")
        return dialog_class(parent, **kwargs)
