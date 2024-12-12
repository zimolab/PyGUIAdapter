"""
@Time    : 2024.12.12
@File    : useful.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 其他一些开发者可以在业务逻辑中调用的函数
"""

from .ucontext import _context


def highlight_parameter(parameter_name: str) -> None:
    """
    高亮显示参数名称所对应的控件，若参数名称不存在，则不产生任何效果。

    Args:
        parameter_name: 需要高亮显示的控件名称

    Returns:
        无返回值
    """
    _context.sig_highlight_parameter.emit(parameter_name)
