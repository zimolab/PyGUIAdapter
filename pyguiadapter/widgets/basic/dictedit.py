from __future__ import annotations

import dataclasses
from typing import Type, TypeVar

from qtpy.QtWidgets import QWidget

from .literaledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType


@dataclasses.dataclass(frozen=True)
class DictEditConfig(PyLiteralEditConfig):
    default_value: dict | None = dataclasses.field(default_factory=dict)
    initial_text: str = "{}"

    @classmethod
    def target_widget_class(cls) -> Type["DictEdit"]:
        return DictEdit


class DictEdit(PyLiteralEdit):
    Self = TypeVar("Self", bound="DictEdit")
    ConfigClass = DictEditConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: DictEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def to_data(self, text: str) -> dict | None:
        if text is None or text.strip() == "":
            return None
        data = super().to_data(text)
        if data is None:
            return None
        if not isinstance(data, dict):
            raise ValueError(f"cannot convert to a dict: {text}")
        return data

    def from_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, dict):
            raise ValueError(f"not a dict: {data}")
        return super().from_data(data)
