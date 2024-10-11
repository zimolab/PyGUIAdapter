import dataclasses
from typing import Optional

from .ucontext import uprint
from ..constants.color import (
    COLOR_INFO,
    COLOR_TERMINAL_TEXT_CLASSIC,
    COLOR_WARNING,
    COLOR_ERROR,
    COLOR_FATAL,
)

# DEFAULT_COLOR_INFO = "#00FF00"
# DEFAULT_COLOR_DEBUG = "#FFFFFF"
# DEFAULT_COLOR_WARNING = "#FFFF00"
# DEFAULT_COLOR_CRITICAL = "#FF0000"
# DEFAULT_COLOR_FATAL = "#A61C00"

_MSG_TMPL = "<p><pre style='color:{color}'>{msg}</pre></p>"


@dataclasses.dataclass
class LoggerConfig(object):
    info_color: str = COLOR_INFO
    debug_color: str = COLOR_TERMINAL_TEXT_CLASSIC
    warning_color: str = COLOR_WARNING
    critical_color: str = COLOR_ERROR
    fatal_color: str = COLOR_FATAL


class Logger(object):
    def __init__(self, confing: Optional[LoggerConfig] = None):
        self._config = confing or LoggerConfig()

    @property
    def config(self) -> LoggerConfig:
        return self._config

    def info(self, msg: str):
        uprint(self._message(self._config.info_color, msg), html=True)

    def debug(self, msg: str):
        uprint(self._message(self._config.debug_color, msg), html=True)

    def warning(self, msg: str):
        uprint(self._message(self._config.warning_color, msg), html=True)

    def critical(self, msg: str):
        uprint(self._message(self._config.critical_color, msg), html=True)

    def fatal(self, msg: str):
        uprint(self._message(self._config.fatal_color, msg), html=True)

    @staticmethod
    def _message(color: str, msg: str):
        # msg = (
        #     msg.replace("\n", "<br>")
        #     .replace("\r\n", "<br>")
        #     .replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        #     .replace(" ", "&nbsp;")
        #     .replace("<", "&lt;")
        #     .replace(">", "&gt;")
        #     .replace("&", "&amp;")
        #     .replace("'", "&apos;")
        #     .replace('"', "&quot;")
        # )
        return _MSG_TMPL.format(color=color, msg=msg)


_global_logger = Logger()


def info(msg: str):
    _global_logger.info(msg)


def debug(msg: str):
    _global_logger.debug(msg)


def warning(msg: str):
    _global_logger.warning(msg)


def critical(msg: str):
    _global_logger.critical(msg)


def fatal(msg: str):
    _global_logger.fatal(msg)
