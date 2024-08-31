from . import FloatLineEdit
from .edit import LineEdit, TextEdit, IntSpinBox, IntLineEdit, FloatSpinBox
from .editor import (
    JsonEditor,
    PyLiteralEditor,
    PyLiteralType,
    DictEditor,
    ListEditor,
    TupleEditor,
    SetEditor,
)
from .path import DirSelect, FileSelect, MultiFileSelect
from ..parser.typenames import (
    TYPE_STR,
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_ANY,
    TYPE_DICT,
    TYPE_LIST,
    TYPE_TUPLE,
    TYPE_SET,
)
from ..types import text_t, int_t, float_t, directory_t, file_t, file_list_t, literal_t

TYPE_TEXT = text_t.__name__
TYPE_INT_T = int_t.__name__
TYPE_FLOAT_T = float_t.__name__
TYPE_DIR_T = directory_t.__name__
TYPE_FILE_T = file_t.__name__
TYPE_FILE_LIST_T = file_list_t.__name__
TYPE_PY_LITERAL_T = literal_t.__name__
TYPE_PY_LITERAL_T_2 = str(PyLiteralType)

BUILTIN_WIDGETS_MAP = {
    TYPE_STR: LineEdit,
    TYPE_TEXT: TextEdit,
    TYPE_INT: IntSpinBox,
    TYPE_INT_T: IntLineEdit,
    TYPE_FLOAT: FloatSpinBox,
    TYPE_FLOAT_T: FloatLineEdit,
    TYPE_DIR_T: DirSelect,
    TYPE_FILE_T: FileSelect,
    TYPE_FILE_LIST_T: MultiFileSelect,
    TYPE_ANY: JsonEditor,
    TYPE_PY_LITERAL_T: PyLiteralEditor,
    TYPE_PY_LITERAL_T_2: PyLiteralEditor,
    TYPE_DICT: DictEditor,
    TYPE_LIST: ListEditor,
    TYPE_TUPLE: TupleEditor,
    TYPE_SET: SetEditor,
}
