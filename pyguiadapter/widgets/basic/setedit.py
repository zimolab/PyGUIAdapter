from __future__ import annotations

import dataclasses
from typing import Type

from qtpy.QtWidgets import QWidget

from .literaledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType


@dataclasses.dataclass(frozen=True)
class SetEditConfig(PyLiteralEditConfig):
    default_value: set | None = None
    initial_text: str = "None"

    @classmethod
    def target_widget_class(cls) -> Type["SetEdit"]:
        return SetEdit


class SetEdit(PyLiteralEdit):
    ConfigClass = SetEditConfig

    def __init__(
        self, parent: QWidget | None, parameter_name: str, config: SetEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def _get_data(self, text: str) -> set | None:
        if text is None or text.strip() == "":
            return None
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, set):
            raise ValueError(f"not a set: {text}")
        return data

    def _set_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, list):
            raise ValueError(f"not a set: {data}")
        return super()._set_data(data)
