from __future__ import annotations

import json
from typing import Dict, Any

from qtpy.QtCore import QObject, Qt
from qtpy.QtGui import QTextCharFormat, QColor
from . import _utils


_UnderlineStyles = {
    "SingleUnderline": QTextCharFormat.UnderlineStyle.SingleUnderline,
    "DashUnderline": QTextCharFormat.UnderlineStyle.DashUnderline,
    "DotLine": QTextCharFormat.UnderlineStyle.DotLine,
    "DashDotLine": QTextCharFormat.UnderlineStyle.DashDotLine,
    "DashDotDotLine": QTextCharFormat.UnderlineStyle.DashDotDotLine,
    "WaveUnderline": QTextCharFormat.UnderlineStyle.WaveUnderline,
    "SpellCheckUnderline": QTextCharFormat.UnderlineStyle.SpellCheckUnderline,
    "NoUnderline": QTextCharFormat.UnderlineStyle.NoUnderline,
}


# noinspection PyPep8Naming
class QSyntaxStyle(QObject):

    _defaultStyle: QSyntaxStyle | None = None

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

        self.m_name: str = ""
        self.m_loaded: bool = False
        self.m_data: Dict[str, QTextCharFormat] = {}

    def load(self, f1: str) -> bool:
        self.m_loaded = False
        try:
            data = json.loads(f1)
            if isinstance(data, dict):
                style_schema = data.get("style-schema", None)
                if isinstance(style_schema, dict):
                    self._processStyleSchema(style_schema)
        except Exception as e:
            print(e)
        return self.m_loaded

    def name(self) -> str:
        return self.m_name

    def isLoaded(self) -> bool:
        return self.m_loaded

    def getFormat(self, name: str) -> QTextCharFormat:
        return self.m_data.get(name, QTextCharFormat())

    def _processStyleSchema(self, style_schema: Dict[str, Any]):
        name = style_schema.get("name", None)
        if not isinstance(name, str) or name.strip() == "":
            return
        styles = style_schema.get("style", None)
        if not isinstance(styles, list):
            return
        self.m_loaded = True

        for style in styles:
            if not isinstance(style, dict):
                continue
            style_name = style.get("name", None)
            if not isinstance(style_name, str) or style_name.strip() == "":
                continue
            style_format = QTextCharFormat()

            background = style.get("background", None)
            if background:
                style_format.setBackground(QColor(str(background)))

            foreground = style.get("foreground", None)
            if foreground:
                style_format.setForeground(QColor(str(foreground)))

            bold = style.get("bold", "")
            if bold == "true":
                style_format.setFontWeight(Qt.Weight.Bold)

            italic = style.get("italic", "")
            if italic == "true":
                style_format.setFontItalic(True)

            underlineStyle = style.get("underlineStyle", "")
            underlineStyle = _UnderlineStyles.get(underlineStyle, "NoUnderline")
            style_format.setUnderlineStyle(underlineStyle)
            self.m_data[style_name] = style_format

    @classmethod
    def defaultStyle(cls) -> "QSyntaxStyle":
        if not isinstance(cls._defaultStyle, QSyntaxStyle):
            cls._defaultStyle = QSyntaxStyle()
        if not cls._defaultStyle.isLoaded():
            return cls._defaultStyle
        c = _utils.read_resource_text("default_style.json")
        ret = cls._defaultStyle.load(c)
        if not ret:
            print("Can't load default style.")
        return cls._defaultStyle
