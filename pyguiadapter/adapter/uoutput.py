import dataclasses
from typing import Optional

from .ucontext import uprint
from ..constants.color import (
    COLOR_INFO,
    COLOR_DEBUG,
    COLOR_WARNING,
    COLOR_FATAL,
    COLOR_CRITICAL,
)

_MSG_TMPL = "<p><pre style='color:{color}'>{msg}</pre></p>"


@dataclasses.dataclass
class LoggerConfig(object):
    info_color: str = COLOR_INFO
    debug_color: str = COLOR_DEBUG
    warning_color: str = COLOR_WARNING
    critical_color: str = COLOR_CRITICAL
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


def info(msg: str) -> None:
    """打印`info`级别的消息。`info`消息颜色值默认为：<b>`#00FF00`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.info(msg)


def debug(msg: str) -> None:
    """打印`debug`级别的消息。`debug`消息颜色值默认为：<b>`#909399`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.debug(msg)


def warning(msg: str) -> None:
    """打印`warning`级别的消息。`warning`消息颜色值默认为：<b>`#FFFF00`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.warning(msg)


def critical(msg: str) -> None:
    """打印`critical`级别的消息。`critical`消息颜色值默认为：<b>`#A61C00`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.critical(msg)


def fatal(msg: str) -> None:
    """打印`fatal`级别的消息。`fatal`消息颜色值默认为：<b>`#FF0000`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.fatal(msg)
