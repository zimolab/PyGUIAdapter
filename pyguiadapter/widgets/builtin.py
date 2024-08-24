from ..types import text_t
from ..parser.typenames import TYPE_STR
from .edit.lineedit import LineEdit
from .edit.textedit import TextEdit


TYPE_TEXT = text_t.__name__

BUILTIN_WIDGETS = {
    TYPE_STR: LineEdit,
    TYPE_TEXT: TextEdit,
}
