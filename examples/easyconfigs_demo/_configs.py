from function2widgets import IntLineEdit
from function2widgets import IntLineEditArgs
from function2widgets import FloatLineEdit
from function2widgets import FloatLineEditArgs
from function2widgets import CheckBox
from function2widgets import CheckBoxArgs
from function2widgets import LineEdit
from function2widgets import LineEditArgs
from function2widgets import TupleEditor
from function2widgets import TupleEditorArgs
from function2widgets import ListEditor
from function2widgets import ListEditorArgs
from function2widgets import DictEditor
from function2widgets import DictEditorArgs
from function2widgets import ColorEdit
from function2widgets import ColorEditArgs
from function2widgets import DateTimeEdit
from function2widgets import DateTimeEditArgs
from function2widgets import DateEdit
from function2widgets import DateEditArgs
from function2widgets import TimeEdit
from function2widgets import TimeEditArgs
from ._constants import *

CONFIGS = {
    
    
    "a": {
        "widget_class": IntLineEdit.__name__,
        "widget_args": IntLineEditArgs(
            parameter_name="AS-IS",
            label=LABEL_A,
            description=DESCRIPTION_A,
            default=DEFAULT_VALUE_A,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_A,
        ),
    },

    
    
    "b": {
        "widget_class": FloatLineEdit.__name__,
        "widget_args": FloatLineEditArgs(
            parameter_name="AS-IS",
            label=LABEL_B,
            description=DESCRIPTION_B,
            default=DEFAULT_VALUE_B,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_B,
        ),
    },

    
    
    "c": {
        "widget_class": CheckBox.__name__,
        "widget_args": CheckBoxArgs(
            parameter_name="AS-IS",
            label=LABEL_C,
            description=DESCRIPTION_C,
            default=DEFAULT_VALUE_C,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_C,
        ),
    },

    
    
    "d": {
        "widget_class": LineEdit.__name__,
        "widget_args": LineEditArgs(
            parameter_name="AS-IS",
            label=LABEL_D,
            description=DESCRIPTION_D,
            default=DEFAULT_VALUE_D,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_D,
        ),
    },

    
    
    "e": {
        "widget_class": TupleEditor.__name__,
        "widget_args": TupleEditorArgs(
            parameter_name="AS-IS",
            label=LABEL_E,
            description=DESCRIPTION_E,
            default=DEFAULT_VALUE_E,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_E,
        ),
    },

    
    
    "f": {
        "widget_class": ListEditor.__name__,
        "widget_args": ListEditorArgs(
            parameter_name="AS-IS",
            label=LABEL_F,
            description=DESCRIPTION_F,
            default=DEFAULT_VALUE_F,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_F,
        ),
    },

    
    
    "g": {
        "widget_class": DictEditor.__name__,
        "widget_args": DictEditorArgs(
            parameter_name="AS-IS",
            label=LABEL_G,
            description=DESCRIPTION_G,
            default=DEFAULT_VALUE_G,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_G,
        ),
    },

    
    
    "color2": {
        "widget_class": ColorEdit.__name__,
        "widget_args": ColorEditArgs(
            parameter_name="AS-IS",
            label=LABEL_COLOR2,
            description=DESCRIPTION_COLOR2,
            default=DEFAULT_VALUE_COLOR2,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_COLOR2,
        ),
    },

    
    
    "h": {
        "widget_class": LineEdit.__name__,
        "widget_args": LineEditArgs(
            parameter_name="AS-IS",
            label=LABEL_H,
            description=DESCRIPTION_H,
            default=DEFAULT_VALUE_H,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_H,
        ),
    },

    
    
    "color": {
        "widget_class": ColorEdit.__name__,
        "widget_args": ColorEditArgs(
            parameter_name="AS-IS",
            label=LABEL_COLOR,
            description=DESCRIPTION_COLOR,
            default=DEFAULT_VALUE_COLOR,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_COLOR,
        ),
    },

    
    
    "datetime1": {
        "widget_class": DateTimeEdit.__name__,
        "widget_args": DateTimeEditArgs(
            parameter_name="AS-IS",
            label=LABEL_DATETIME1,
            description=DESCRIPTION_DATETIME1,
            default=DEFAULT_VALUE_DATETIME1,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_DATETIME1,
        ),
    },

    
    
    "date1": {
        "widget_class": DateEdit.__name__,
        "widget_args": DateEditArgs(
            parameter_name="AS-IS",
            label=LABEL_DATE1,
            description=DESCRIPTION_DATE1,
            default=DEFAULT_VALUE_DATE1,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_DATE1,
        ),
    },

    
    
    "time1": {
        "widget_class": TimeEdit.__name__,
        "widget_args": TimeEditArgs(
            parameter_name="AS-IS",
            label=LABEL_TIME1,
            description=DESCRIPTION_TIME1,
            default=DEFAULT_VALUE_TIME1,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_TIME1,
        ),
    },

    
    
    "datetime2": {
        "widget_class": DateTimeEdit.__name__,
        "widget_args": DateTimeEditArgs(
            parameter_name="AS-IS",
            label=LABEL_DATETIME2,
            description=DESCRIPTION_DATETIME2,
            default=DEFAULT_VALUE_DATETIME2,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_DATETIME2,
        ),
    },

    
    
    "date2": {
        "widget_class": DateEdit.__name__,
        "widget_args": DateEditArgs(
            parameter_name="AS-IS",
            label=LABEL_DATE2,
            description=DESCRIPTION_DATE2,
            default=DEFAULT_VALUE_DATE2,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_DATE2,
        ),
    },

    
    
    "time2": {
        "widget_class": TimeEdit.__name__,
        "widget_args": TimeEditArgs(
            parameter_name="AS-IS",
            label=LABEL_TIME2,
            description=DESCRIPTION_TIME2,
            default=DEFAULT_VALUE_TIME2,
            default_value_description=DEFAULT_VALUE_DESCRIPTION_TIME2,
        ),
    },

}