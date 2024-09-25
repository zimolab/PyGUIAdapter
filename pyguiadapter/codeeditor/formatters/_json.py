import json
import warnings
from typing import Optional

from ..base import BaseCodeFormatter


class JsonFormatter(BaseCodeFormatter):

    def __init__(self, indent: int = 4):
        self._indent = indent

    @property
    def indent(self) -> int:
        return self._indent

    @indent.setter
    def indent(self, value: int):
        if value < 0:
            warnings.warn(f"indent must be greater than or equals to 0, got: {value}")
            return
        self._indent = value

    def format_code(self, text: str) -> Optional[str]:
        try:
            return json.dumps(json.loads(text), indent=self._indent, ensure_ascii=False)
        except Exception as e:
            warnings.warn(f"failed to format code: {e}")
            return None
