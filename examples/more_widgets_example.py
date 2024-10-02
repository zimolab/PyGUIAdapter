import enum
from datetime import datetime, date, time

from typing import List, Tuple, Literal

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.extend_types import (
    int_t,
    int_dial_t,
    int_slider_t,
    float_t,
    file_t,
    directory_t,
    files_t,
    color_t,
    string_list_t,
    plain_dict_t,
    json_obj_t,
    text_t,
    key_sequence_t,
    choices_t,
    choice_t,
)


class WeekDays(enum.Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


def more_widgets_example(
    arg1: int,
    arg2: float,
    arg3: str,
    arg4: bool,
    arg5: List[int],
    arg6: Tuple,
    arg7: dict,
    arg9: set,
    arg10: int_t,
    arg11: int_dial_t,
    arg12: int_slider_t,
    arg13: float_t,
    arg14: file_t,
    arg15: directory_t,
    arg16: files_t,
    arg17: Literal["a", "b", "c"],
    arg18: color_t,
    arg19: string_list_t,
    arg20: plain_dict_t,
    arg21: json_obj_t,
    arg22: text_t,
    arg23: datetime,
    arg24: date,
    arg25: time,
    arg26: key_sequence_t,
    arg27: choices_t,
    arg28: choice_t,
    arg29: WeekDays,
):
    """
    @params

    [arg27]
    choices = ["a", "b", "c", "d", "e", "f"]
    columns = 2

    [arg28]
    choices = ["a", "b", "c", "d", "e", "f"]
    editable = true

    @end
    """


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(more_widgets_example)
    adapter.run()
