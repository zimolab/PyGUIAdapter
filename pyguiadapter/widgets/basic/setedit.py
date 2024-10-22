import dataclasses

from qtpy.QtWidgets import QWidget
from typing import Type, Optional, Any

from .pyliteraledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class SetEditConfig(PyLiteralEditConfig):
    default_value: Optional[set] = dataclasses.field(default_factory=set)
    initial_text: str = "{}"

    @classmethod
    def target_widget_class(cls) -> Type["SetEdit"]:
        return SetEdit


class SetEdit(PyLiteralEdit):
    ConfigClass = SetEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: SetEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        if value == "":
            return
        type_check(value, allowed_types=(set,), allow_none=True)

    def _get_data(self, text: str) -> Optional[set]:
        text = text.strip()
        if text is None or text == "":
            return None
        if text == "{}":
            return set()
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, set):
            raise ValueError(f"not a set")
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
