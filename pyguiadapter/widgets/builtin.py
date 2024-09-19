from datetime import datetime, date, time

from qtpy.QtGui import QColor

from .basic import (
    PyLiteralEdit,
    PyLiteralType,
    DictEdit,
    ListEdit,
    TupleEdit,
    SetEdit,
    LineEdit,
    IntSpinBox,
    FloatSpinBox,
    BoolBox,
    EnumSelect,
    ExclusiveChoiceBox,
    DateTimeEdit,
    DateEdit,
    TimeEdit,
)
from .extend import (
    IntLineEdit,
    FloatLineEdit,
    JsonEdit,
    TextEdit,
    ChoiceBox,
    MultiChoiceBox,
    Slider,
    Dial,
    ColorTuplePicker,
    ColorHexPicker,
    ColorPicker,
    KeySequenceEdit,
    StringListEdit,
    PlainDictEdit,
    DirSelect,
    FileSelect,
    MultiFileSelect,
)
from ..parser.typenames import (
    TYPE_STR,
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_ANY,
    TYPE_OBJECT,
    TYPE_DICT,
    TYPE_LIST,
    TYPE_TUPLE,
    TYPE_SET,
    TYPE_BOOL,
    TYPING_ANY,
    TYPING_LITERAL,
    TYPING_UNION,
    TYPING_DICT,
    TYPING_LIST,
    TYPING_TUPLE,
    TYPING_SET,
    TYPE_MAPPING,
    TYPE_MUTABLE_MAPPING,
    TYPE_MUTABLE_SET,
    TYPING_TYPED_DICT,
)
from ..types import (
    text_t,
    int_t,
    float_t,
    directory_t,
    file_t,
    files_t,
    json_obj_t,
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
TYPE_FILES_T = files_t.__name__
TYPE_JSON_OBJ_T = json_obj_t.__name__
TYPE_PY_LITERAL = str(PyLiteralType)
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
    TYPE_INT_T: IntLineEdit,
    TYPE_FLOAT: FloatSpinBox,
    TYPE_FLOAT_T: FloatLineEdit,
    TYPE_DIR_T: DirSelect,
    TYPE_FILE_T: FileSelect,
    TYPE_FILES_T: MultiFileSelect,
    TYPE_JSON_OBJ_T: JsonEdit,
    TYPE_ANY: PyLiteralEdit,
    TYPING_ANY: PyLiteralEdit,
    TYPE_PY_LITERAL: PyLiteralEdit,
    TYPING_UNION: PyLiteralEdit,
    TYPE_OBJECT: PyLiteralEdit,
    TYPE_DICT: DictEdit,
    TYPING_DICT: DictEdit,
    TYPE_MAPPING: DictEdit,
    TYPE_MUTABLE_MAPPING: DictEdit,
    TYPING_TYPED_DICT: DictEdit,
    TYPE_LIST: ListEdit,
    TYPING_LIST: ListEdit,
    TYPE_TUPLE: TupleEdit,
    TYPING_TUPLE: TupleEdit,
    TYPE_SET: SetEdit,
    TYPING_SET: SetEdit,
    TYPE_MUTABLE_SET: SetEdit,
    TYPING_LITERAL: ExclusiveChoiceBox,
    TYPE_CHOICE_T: ChoiceBox,
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
    EnumSelect._enum_type_mapping_rule,
    DictEdit._dict_mapping_rule,
]
