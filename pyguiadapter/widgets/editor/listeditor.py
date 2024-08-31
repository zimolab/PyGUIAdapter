from __future__ import annotations

import copy
import dataclasses
from typing import Type, TypeVar

from qtpy.QtWidgets import QWidget

from . import PyLiteralType
from .literaleditor import PyLiteralEditor, PyLiteralEditorConfig


@dataclasses.dataclass(frozen=True)
class ListEditorConfig(PyLiteralEditorConfig):
    default_value: dict | None = None
    initial_text: str = "[]"

    @classmethod
    def target_widget_class(cls) -> Type["ListEditor"]:
        return ListEditor


class ListEditor(PyLiteralEditor):
    Self = TypeVar("Self", bound="ListEditor")
    ConfigClass = ListEditorConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: ListEditorConfig
    ):
        super().__init__(parent, parameter_name, config)

    def to_data(self, text: str) -> list | None:
        if text is None or text.strip() == "":
            return None
        data = super().to_data(text)
        if data is None:
            return None
        if not isinstance(data, list):
            raise ValueError(f"cannot convert to a list: {text}")
        return data

    def from_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, list):
            raise ValueError(f"not a list: {data}")
        return super().from_data(data)
