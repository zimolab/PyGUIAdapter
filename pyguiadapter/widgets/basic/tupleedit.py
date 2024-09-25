import dataclasses
from typing import Type, Optional

from qtpy.QtWidgets import QWidget

from .literaledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType


@dataclasses.dataclass(frozen=True)
class TupleEditConfig(PyLiteralEditConfig):
    default_value: Optional[tuple] = dataclasses.field(default_factory=tuple)
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

    def _get_data(self, text: str) -> Optional[tuple]:
        if text is None or text.strip() == "":
            return None
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, tuple):
            raise ValueError(f"cannot convert to a tuple: {text}")
        return data

    def _set_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, tuple):
            raise ValueError(f"not a tuple: {data}")
        return super()._set_data(data)
