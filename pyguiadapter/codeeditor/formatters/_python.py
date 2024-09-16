from __future__ import annotations

import warnings

from yapf.yapflib.yapf_api import FormatCode

from ..base import BaseCodeFormatter


class PythonFormatter(BaseCodeFormatter):
    def format_code(self, text: str) -> str | None:
        try:
            formatted, changed = FormatCode(text)
        except Exception as e:
            warnings.warn(f"failed to format code: {e}")
            return None
        else:
            if changed:
                return formatted
            return None
