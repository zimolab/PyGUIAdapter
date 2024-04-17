import enum
import html
from datetime import datetime

from .uprint import uprint

DEFAULT_COLOR_INFO = "#00FF00"
DEFAULT_COLOR_DEBUG = "#FFFFFF"
DEFAULT_COLOR_WARNING = "#FFFF00"
DEFAULT_COLOR_CRITICAL = "#FF0000"
DEFAULT_COLOR_FATAL = "#A61C00"


class LogLevel(enum.Enum):
    INFO = 0
    DEBUG = 1
    WARNING = 2
    CRITICAL = 3
    FATAL = 4


__colored_msg_template = "<font color=%s>%s</font>"
__timestamp = False
__timestamp_pattern = "%Y-%m-%d %H:%M:%S"
__print_func = uprint
__additional_newline = False
__color_info = DEFAULT_COLOR_INFO
__color_warning = DEFAULT_COLOR_WARNING
__color_debug = DEFAULT_COLOR_DEBUG
__color_critical = DEFAULT_COLOR_CRITICAL
__color_fatal = DEFAULT_COLOR_FATAL


def set_print_func(print_func):
    global __print_func
    __print_func = print_func


def add_additional_nl(enabled: bool):
    global __additional_newline
    __additional_newline = enabled


def enable_timestamp(enabled: bool):
    global __timestamp
    __timestamp = enabled


def set_timestamp_format(timestamp_format: str):
    global __timestamp_pattern
    __timestamp_pattern = timestamp_format


def set_color_msg_template(color_msg_tpl: str):
    global __colored_msg_template
    __colored_msg_template = color_msg_tpl


def set_info_color(color: str):
    global __color_info
    __color_info = color


def set_warning_color(color: str):
    global __color_warning
    __color_warning = color


def set_debug_color(color: str):
    global __color_debug
    __color_debug = color


def set_critical_color(color: str):
    global __color_critical
    __color_critical = color


def set_fatal_color(color: str):
    global __color_fatal
    __color_fatal = color


def _message(msg: str, color: str) -> str:
    return __colored_msg_template % (color, msg)


def log(
    level: LogLevel,
    msg: str,
    timestamp: bool = None,
    timestamp_pattern: str = None,
    additional_nl: bool = None,
    print_func: callable = None,
):
    global __timestamp, __timestamp_pattern, __print_func, __additional_newline
    if timestamp is None:
        timestamp = __timestamp
    if timestamp_pattern is None:
        timestamp_pattern = __timestamp_pattern
    if additional_nl is None:
        additional_nl = __additional_newline
    if print_func is None:
        print_func = __print_func

    global __color_info, __color_warning, __color_debug, __color_critical, __color_fatal

    msg = html.escape(msg)
    if level == LogLevel.INFO:
        msg = _message(msg, __color_info)
    elif level == LogLevel.DEBUG:
        msg = _message(msg, __color_debug)
    elif level == LogLevel.WARNING:
        msg = _message(msg, __color_warning)
    elif level == LogLevel.CRITICAL:
        msg = _message(msg, __color_critical)
    elif level == LogLevel.FATAL:
        msg = _message(msg, __color_critical)
    elif level == LogLevel.FATAL:
        msg = _message(msg, __color_fatal)
    else:
        pass

    if timestamp:
        timestamp_str = datetime.now().strftime(timestamp_pattern)
        msg = f"[{timestamp_str}] {msg}"
    print_func(f"{msg}", html=True)
    if additional_nl:
        print_func(html=False)


def info(
    msg: str,
    timestamp: bool = None,
    timestamp_pattern: str = None,
    additional_nl: bool = None,
    print_func: callable = None,
):
    log(
        LogLevel.INFO,
        msg,
        timestamp=timestamp,
        timestamp_pattern=timestamp_pattern,
        additional_nl=additional_nl,
        print_func=print_func,
    )


def debug(
    msg: str,
    timestamp: bool = None,
    timestamp_pattern: str = None,
    additional_nl: bool = None,
    print_func: callable = None,
):
    log(
        LogLevel.DEBUG,
        msg,
        timestamp=timestamp,
        timestamp_pattern=timestamp_pattern,
        additional_nl=additional_nl,
        print_func=print_func,
    )


def warning(
    msg: str,
    timestamp: bool = None,
    timestamp_pattern: str = None,
    additional_nl: bool = None,
    print_func: callable = None,
):
    log(
        LogLevel.WARNING,
        msg,
        timestamp=timestamp,
        timestamp_pattern=timestamp_pattern,
        additional_nl=additional_nl,
        print_func=print_func,
    )


def critical(
    msg: str,
    timestamp: bool = None,
    timestamp_pattern: str = None,
    additional_nl: bool = None,
    print_func: callable = None,
):
    log(
        LogLevel.CRITICAL,
        msg,
        timestamp=timestamp,
        timestamp_pattern=timestamp_pattern,
        additional_nl=additional_nl,
        print_func=print_func,
    )


def fatal(
    msg: str,
    timestamp: bool = None,
    timestamp_pattern: str = None,
    additional_nl: bool = None,
    print_func: callable = None,
):
    log(
        LogLevel.FATAL,
        msg,
        timestamp=timestamp,
        timestamp_pattern=timestamp_pattern,
        additional_nl=additional_nl,
        print_func=print_func,
    )
