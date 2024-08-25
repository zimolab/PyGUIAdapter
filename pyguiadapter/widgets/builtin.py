from . import FloatLineEdit
from ..parser.typenames import TYPE_STR, TYPE_INT, TYPE_FLOAT
from ..types import text_t, int_t, float_t
from .edit import LineEdit, TextEdit, IntSpinBox, IntLineEdit, FloatSpinBox


TYPE_TEXT = text_t.__name__
TYPE_INT_T = int_t.__name__
TYPE_FLOAT_T = float_t.__name__

BUILTIN_WIDGETS = {
    TYPE_STR: LineEdit,
    TYPE_TEXT: TextEdit,
    TYPE_INT: IntSpinBox,
    TYPE_INT_T: IntLineEdit,
    TYPE_FLOAT: FloatSpinBox,
    TYPE_FLOAT_T: FloatLineEdit,
}
