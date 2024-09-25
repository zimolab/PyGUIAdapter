import dataclasses
from typing import Type, Optional

from qtpy.QtWidgets import QWidget

from .literaledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType


@dataclasses.dataclass(frozen=True)
class ListEditConfig(PyLiteralEditConfig):
    default_value: Optional[list] = dataclasses.field(default_factory=list)
    initial_text: str = "[]"

    @classmethod
    def target_widget_class(cls) -> Type["ListEdit"]:
        return ListEdit


class ListEdit(PyLiteralEdit):
    ConfigClass = ListEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: ListEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def _get_data(self, text: str) -> Optional[list]:
        if text is None or text.strip() == "":
            return None
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, list):
            raise ValueError(f"cannot convert to a list: {text}")
        return data

    def _set_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, list):
            raise ValueError(f"not a list: {data}")
        return super()._set_data(data)
