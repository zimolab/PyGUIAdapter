from __future__ import annotations

import copy
import dataclasses
from typing import Type, TypeVar

from qtpy.QtWidgets import QWidget

from . import PyLiteralType
from .literaleditor import PyLiteralEditor, PyLiteralEditorConfig


@dataclasses.dataclass(frozen=True)
class TupleEditorConfig(PyLiteralEditorConfig):
    default_value: dict | None = None
    initial_text: str = "()"

    @classmethod
    def target_widget_class(cls) -> Type["TupleEditor"]:
        return TupleEditor


class TupleEditor(PyLiteralEditor):
    Self = TypeVar("Self", bound="TupleEditor")
    ConfigClass = TupleEditorConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: TupleEditorConfig
    ):
        super().__init__(parent, parameter_name, config)

    def to_data(self, text: str) -> tuple | None:
        if text is None or text.strip() == "":
            return None
        data = super().to_data(text)
        if data is None:
            return None
        if not isinstance(data, tuple):
            raise ValueError(f"cannot convert to a tuple: {text}")
        return data

    def from_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, tuple):
            raise ValueError(f"not a tuple: {data}")
        return super().from_data(data)
