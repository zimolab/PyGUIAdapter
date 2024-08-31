from __future__ import annotations

import copy
import dataclasses
from typing import Type, TypeVar

from qtpy.QtWidgets import QWidget

from . import PyLiteralType
from .literaleditor import PyLiteralEditor, PyLiteralEditorConfig


@dataclasses.dataclass(frozen=True)
class DictEditorConfig(PyLiteralEditorConfig):
    default_value: dict | None = None
    initial_text: str = "{}"

    @classmethod
    def target_widget_class(cls) -> Type["DictEditor"]:
        return DictEditor


class DictEditor(PyLiteralEditor):
    Self = TypeVar("Self", bound="DictEditor")
    ConfigClass = DictEditorConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: DictEditorConfig
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
