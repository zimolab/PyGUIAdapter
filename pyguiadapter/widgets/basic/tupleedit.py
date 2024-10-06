import dataclasses

from qtpy.QtWidgets import QWidget
from typing import Type, Optional, Any

from .literaledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType
from ...utils import type_check


@dataclasses.dataclass(frozen=True)
class TupleEditConfig(PyLiteralEditConfig):
    default_value: Optional[tuple] = ()
    initial_text: str = "()"

    @classmethod
    def target_widget_class(cls) -> Type["TupleEdit"]:
        return TupleEdit


class TupleEdit(PyLiteralEdit):
    ConfigClass = TupleEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: TupleEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        type_check(value, (tuple,), allow_none=True)

    def _get_data(self, text: str) -> Optional[tuple]:
        text = text.strip()
        if text is None or text == "":
            return None
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, tuple):
            raise ValueError(f"not a tuple")

    def _set_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, tuple):
            raise ValueError(f"not a tuple: {data}")
        return super()._set_data(data)
