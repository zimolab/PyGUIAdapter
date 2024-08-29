from . import FloatLineEdit
from ..parser.typenames import TYPE_STR, TYPE_INT, TYPE_FLOAT, TYPE_ANY
from ..types import text_t, int_t, float_t, directory_t, file_t, file_list_t
from .edit import LineEdit, TextEdit, IntSpinBox, IntLineEdit, FloatSpinBox
from .path import DirSelect, FileSelect, MultiFileSelect
from .editor import AnyEditor

TYPE_TEXT = text_t.__name__
TYPE_INT_T = int_t.__name__
TYPE_FLOAT_T = float_t.__name__
TYPE_DIR_T = directory_t.__name__
TYPE_FILE_T = file_t.__name__
TYPE_FILE_LIST_T = file_list_t.__name__

BUILTIN_WIDGETS = {
    TYPE_STR: LineEdit,
    TYPE_TEXT: TextEdit,
    TYPE_INT: IntSpinBox,
    TYPE_INT_T: IntLineEdit,
    TYPE_FLOAT: FloatSpinBox,
    TYPE_FLOAT_T: FloatLineEdit,
    TYPE_DIR_T: DirSelect,
    TYPE_FILE_T: FileSelect,
    TYPE_FILE_LIST_T: MultiFileSelect,
    TYPE_ANY: AnyEditor,
}
