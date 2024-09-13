from datetime import datetime, date, time

from qtpy.QtGui import QColor

from .basic import (
    JsonEdit,
    PyLiteralEdit,
    PyLiteralType,
    DictEdit,
    ListEdit,
    TupleEdit,
    SetEdit,
)
from .basic import (
    LineEdit,
    TextEdit,
    IntSpinBox,
    IntLineEdit,
    FloatSpinBox,
    FloatLineEdit,
    BoolBox,
    BinStateSelect,
    EnumSelect,
)
from .extend import (
    ExclusiveChoiceBox,
    ComboBox,
    MultiChoiceBox,
    Slider,
    Dial,
    DateTimeEdit,
    DateEdit,
    TimeEdit,
    ColorTuplePicker,
    ColorHexPicker,
    ColorPicker,
    KeySequenceEdit,
    StringListEdit,
    PlainDictEdit,
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
    TYPE_BOOL,
    TYPE_LITERAL,
)
from ..types import (
    text_t,
    int_t,
    float_t,
    directory_t,
    file_t,
    file_list_t,
    py_literal_t,
    bin_state_t,
    choice_t,
    choices_t,
    int_slider_t,
    int_dial_t,
    color_tuple_t,
    color_hex_t,
    key_sequence_t,
    string_list_t,
    plain_dict_t,
)

TYPE_TEXT = text_t.__name__
TYPE_INT_T = int_t.__name__
TYPE_FLOAT_T = float_t.__name__
TYPE_DIR_T = directory_t.__name__
TYPE_FILE_T = file_t.__name__
TYPE_FILE_LIST_T = file_list_t.__name__
TYPE_PY_LITERAL_T = py_literal_t.__name__
TYPE_PY_LITERAL_T_2 = str(PyLiteralType)
TYPE_BIN_T = bin_state_t.__name__
TYPE_CHOICE_T = choice_t.__name__
TYPE_CHOICES_T = choices_t.__name__
TYPE_SLIDER_INT_T = int_slider_t.__name__
TYPE_DIAL_INT_T = int_dial_t.__name__
TYPE_DATETIME = datetime.__name__
TYPE_DATE = date.__name__
TYPE_TIME = time.__name__
TYPE_COLOR_TUPLE = color_tuple_t.__name__
TYPE_COLOR_HEX = color_hex_t.__name__
# noinspection SpellCheckingInspection
TYPE_QCOLOR = QColor.__name__
TYPE_KEY_SEQUENCE_T = key_sequence_t.__name__
TYPE_STRING_LIST_T = string_list_t.__name__
TYPE_PLAIN_DICT_T = plain_dict_t.__name__

BUILTIN_WIDGETS_MAP = {
    TYPE_STR: LineEdit,
    TYPE_TEXT: TextEdit,
    TYPE_INT: IntSpinBox,
    TYPE_BOOL: BoolBox,
    TYPE_BIN_T: BinStateSelect,
    TYPE_INT_T: IntLineEdit,
    TYPE_FLOAT: FloatSpinBox,
    TYPE_FLOAT_T: FloatLineEdit,
    TYPE_DIR_T: DirSelect,
    TYPE_FILE_T: FileSelect,
    TYPE_FILE_LIST_T: MultiFileSelect,
    TYPE_ANY: JsonEdit,
    TYPE_PY_LITERAL_T: PyLiteralEdit,
    TYPE_PY_LITERAL_T_2: PyLiteralEdit,
    TYPE_DICT: DictEdit,
    TYPE_LIST: ListEdit,
    TYPE_TUPLE: TupleEdit,
    TYPE_SET: SetEdit,
    TYPE_LITERAL: ExclusiveChoiceBox,
    TYPE_CHOICE_T: ComboBox,
    TYPE_CHOICES_T: MultiChoiceBox,
    TYPE_SLIDER_INT_T: Slider,
    TYPE_DIAL_INT_T: Dial,
    TYPE_DATETIME: DateTimeEdit,
    TYPE_DATE: DateEdit,
    TYPE_TIME: TimeEdit,
    TYPE_COLOR_TUPLE: ColorTuplePicker,
    TYPE_COLOR_HEX: ColorHexPicker,
    TYPE_QCOLOR: ColorPicker,
    TYPE_KEY_SEQUENCE_T: KeySequenceEdit,
    TYPE_STRING_LIST_T: StringListEdit,
    TYPE_PLAIN_DICT_T: PlainDictEdit,
}

# noinspection PyProtectedMember
BUILTIN_WIDGETS_MAPPING_RULES = [
    EnumSelect._rule_map_enum_type,
]
