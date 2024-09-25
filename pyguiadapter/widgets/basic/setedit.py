import dataclasses
from typing import Type, Optional

from qtpy.QtWidgets import QWidget

from .literaledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType


@dataclasses.dataclass(frozen=True)
class SetEditConfig(PyLiteralEditConfig):
    default_value: Optional[set] = dataclasses.field(default_factory=set)
    initial_text: str = "None"

    @classmethod
    def target_widget_class(cls) -> Type["SetEdit"]:
        return SetEdit


class SetEdit(PyLiteralEdit):
    ConfigClass = SetEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: SetEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def _get_data(self, text: str) -> Optional[set]:
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
        if not isinstance(data, set):
            raise ValueError(f"not a set: {data}")
        set_str = str(data)
        if set_str.strip() == "set()":
            return "{}"
        return set_str
