from ..parser.typenames import TYPE_STR
from ..types import text_t
from .edit import LineEdit, TextEdit


TYPE_TEXT = text_t.__name__

BUILTIN_WIDGETS = {
    TYPE_STR: LineEdit,
    TYPE_TEXT: TextEdit,
}
