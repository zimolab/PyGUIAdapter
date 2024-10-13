"""
该模块主要实现了消息打印功能，开发者可以在函数中使用该模块提供的函数和类，向函数窗口中打印消息。
"""

import dataclasses
import os.path
from typing import Optional, Union, Dict, Any

from .ucontext import uprint
from ..constants.color import (
    COLOR_INFO,
    COLOR_DEBUG,
    COLOR_WARNING,
    COLOR_FATAL,
    COLOR_CRITICAL,
)
from ..utils import io, to_base64

_MSG_TMPL = "<p><pre style='color:{color}'>{msg}</pre></p>"


@dataclasses.dataclass
class LoggerConfig(object):
    """
    `Logger`的配置类，用于配置`Logger`的颜色等属性。
    包含以下属性：

    + `info_color`: `info`级别消息的颜色
    + `debug_color`: `debug`级别消息的颜色
    + `warning_color`: `warning`级别消息的颜色
    + `critical_color`: `critical`级别消息的颜色
    + `fatal_color`: `fatal`级别消息的颜色

    """

    info_color: str = COLOR_INFO
    debug_color: str = COLOR_DEBUG
    warning_color: str = COLOR_WARNING
    critical_color: str = COLOR_CRITICAL
    fatal_color: str = COLOR_FATAL


class Logger(object):
    """
    该类用于向函数执行窗口的`输出浏览器`区域打印日志消息。不同级别的日志消息，主要以颜色进行区分。可以使用`LoggerConfig`实例指定各消息级别的颜色值。

    示例:

    ```python
    from pyguiadapter.adapter import GUIAdapter
    from pyguiadapter.adapter.uoutput import Logger, LoggerConfig

    logger = Logger(
        config=LoggerConfig(
            info_color="green",
            debug_color="blue",
            warning_color="yellow",
            critical_color="red",
            fatal_color="magenta",
        )
    )


    def output_log_msg(
        info_msg: str = "info message",
        debug_msg: str = "debug message",
        warning_msg: str = "warning message",
        critical_msg: str = "critical message",
        fatal_msg: str = "fatal message",
    ):

        logger.info(info_msg)
        logger.debug(debug_msg)
        logger.warning(warning_msg)
        logger.critical(critical_msg)
        logger.fatal(fatal_msg)

    if __name__ == "__main__":
        adapter = GUIAdapter()
        adapter.add(output_log_msg)
        adapter.run()
    ```

    结果：
    ![logger example](/assets/logger_example.png)
    """

    def __init__(self, config: Optional[LoggerConfig] = None):
        self._config = config or LoggerConfig()

    @property
    def config(self) -> LoggerConfig:
        return self._config

    def info(self, msg: str) -> None:
        """打印`info`级别的消息。

        Args:
            msg: 要打印的消息

        Returns:
            无返回值
        """
        uprint(self._message(self._config.info_color, msg), html=True)

    def debug(self, msg: str) -> None:
        """打印`debug`级别的消息。

        Args:
            msg: 要打印的消息

        Returns:
            无返回值
        """
        uprint(self._message(self._config.debug_color, msg), html=True)

    def warning(self, msg: str) -> None:
        """打印`warning`级别的消息。

        Args:
            msg: 要打印的消息

        Returns:
            无返回值
        """
        uprint(self._message(self._config.warning_color, msg), html=True)

    def critical(self, msg: str) -> None:
        """打印`critical`级别的消息。

        Args:
            msg: 要打印的消息

        Returns:
            无返回值
        """
        uprint(self._message(self._config.critical_color, msg), html=True)

    def fatal(self, msg: str) -> None:
        """打印`fatal`级别的消息。

        Args:
            msg: 要打印的消息

        Returns:
            无返回值
        """
        uprint(self._message(self._config.fatal_color, msg), html=True)

    @staticmethod
    def _message(color: str, msg: str):
        return _MSG_TMPL.format(color=color, msg=msg)


_global_logger = Logger()


def info(msg: str) -> None:
    """模块级函数。打印`info`级别的消息。`info`消息颜色值默认为：<b>`#00FF00`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.info(msg)


def debug(msg: str) -> None:
    """模块级函数。打印`debug`级别的消息。`debug`消息颜色值默认为：<b>`#909399`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.debug(msg)


def warning(msg: str) -> None:
    """模块级函数。打印`warning`级别的消息。`warning`消息颜色值默认为：<b>`#FFFF00`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.warning(msg)


def critical(msg: str) -> None:
    """模块级函数。打印`critical`级别的消息。`critical`消息颜色值默认为：<b>`#A61C00`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.critical(msg)


def fatal(msg: str) -> None:
    """模块级函数。打印`fatal`级别的消息。`fatal`消息颜色值默认为：<b>`#FF0000`</b>。

    Args:
        msg: 要打印的消息

    Returns:
        无返回值
    """
    _global_logger.fatal(msg)


def _join_props(props: Dict[str, Any]):
    return " ".join([f'{k}="{v}"' for k, v in props.items() if v is not None])


def _make_img_url(img: str, props: Dict[str, Any]) -> str:
    return f'<img src="{os.path.abspath(img)}"  {_join_props(props)} />'


def _make_embed_img_url(img: bytes, img_type: str, props: Dict[str, Any]) -> str:
    return f'<img src="data:image/{img_type};base64,{to_base64(img)}"  {_join_props(props)} />'


def print_image(
    img: Union[str, bytes],
    img_type: str = "jpeg",
    embed_base64: bool = False,
    width: Optional[int] = None,
    height: Optional[int] = None,
    centered: bool = True,
) -> None:
    """
    模块级函数。打印图片。

    Args:
        img: 待打印的图片。可以为图片文件的路径（`str`）或图片的二进制数据（`bytes`）
        img_type: 图片类型。
        embed_base64: 是否使用`data url`（`base64格式`）嵌入图片。传入二进制图片数据时，将忽略此参数。
        width: 图片的宽度。若未指定，则显示图片的原始宽度。
        height: 图片的高度。若未指定，则显示图片的原始高度。
        centered: 是否将图片居中显示。

    Returns:
        无返回值。
    """
    props = {
        "width": width,
        "height": height,
    }
    uprint("print image...")
    uprint("<p>some text</p>", html=True)
    if isinstance(img, str):
        if not embed_base64:
            url = _make_img_url(img, props)
        else:
            url = _make_embed_img_url(io.read_file(img), img_type, props)
    else:
        url = _make_embed_img_url(img, img_type, props)
    if centered:
        url = f'<br /><div style="text-align:center;">{url}</div><br />'
    else:
        url = f"<br /><div>{url}</div><br />"
    uprint(url, html=True)
    del url
