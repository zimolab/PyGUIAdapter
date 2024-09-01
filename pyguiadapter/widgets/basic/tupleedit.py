from __future__ import annotations

import dataclasses
from typing import Type, TypeVar

from qtpy.QtWidgets import QWidget

from .literaledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType


@dataclasses.dataclass(frozen=True)
class TupleEditConfig(PyLiteralEditConfig):
    default_value: dict | None = None
    initial_text: str = "()"

    @classmethod
    def target_widget_class(cls) -> Type["TupleEdit"]:
        return TupleEdit


class TupleEdit(PyLiteralEdit):
    Self = TypeVar("Self", bound="TupleEdit")
    ConfigClass = TupleEditConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: TupleEditConfig
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
