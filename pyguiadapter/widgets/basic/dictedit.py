import dataclasses
from typing import Type, Optional, Any

from qtpy.QtWidgets import QWidget

from .literaledit import PyLiteralEdit, PyLiteralEditConfig, PyLiteralType
from ... import utils
from ...exceptions import ParameterError
from ...fn import ParameterInfo


@dataclasses.dataclass(frozen=True)
class DictEditConfig(PyLiteralEditConfig):
    default_value: Optional[dict] = dataclasses.field(default_factory=dict)
    initial_text: str = "{}"

    @classmethod
    def target_widget_class(cls) -> Type["DictEdit"]:
        return DictEdit


class DictEdit(PyLiteralEdit):
    ConfigClass = DictEditConfig

    def __init__(
        self, parent: Optional[QWidget], parameter_name: str, config: DictEditConfig
    ):
        super().__init__(parent, parameter_name, config)

    def check_value_type(self, value: Any):
        if value is None:
            return
        if not isinstance(value, dict):
            raise ParameterError(
                parameter_name=self.parameter_name,
                message=f"value must be a dict, but got {type(value)}",
            )

    def _get_data(self, text: str) -> Optional[dict]:
        if text is None or text.strip() == "":
            return None
        data = super()._get_data(text)
        if data is None:
            return None
        if not isinstance(data, dict):
            raise ValueError(f"cannot convert to a dict: {text}")
        return data

    def _set_data(self, data: PyLiteralType) -> str:
        if data is None:
            return "None"
        if isinstance(data, str) and data.strip() == "":
            return "None"
        if not isinstance(data, dict):
            raise ValueError(f"not a dict: {data}")
        return super()._set_data(data)

    @classmethod
    def _dict_mapping_rule(
        cls, parameter_info: ParameterInfo
    ) -> Optional[Type["DictEdit"]]:
        return DictEdit if utils.is_subclass_of(parameter_info.type, dict) else None
