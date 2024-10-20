"""
@Time    : 2024.10.20
@File    : filedialog.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 提供文件选择对话框的相关工具函数
"""

from typing import List, Optional

from qtpy import compat
from qtpy.QtCore import QUrl
from qtpy.QtWidgets import QWidget, QFileDialog


def get_existing_directory(
    parent: Optional[QWidget] = None,
    title: str = "Open Directory",
    start_dir: str = "",
) -> Optional[str]:
    """
    弹出选择目录对话框，获取已存在的目录路径

    Args:
        parent: 父窗口
        title:  对话框标题
        start_dir: 起始目录

    Returns:
        用户选择的目录路径，如果用户取消选择，则返回None。

    """
    return compat.getexistingdirectory(parent, title, start_dir) or None


def get_existing_directory_url(
    parent: Optional[QWidget] = None,
    title: str = "Open Directory URL",
    start_dir: Optional[QUrl] = None,
    supported_schemes: Optional[List[str]] = None,
) -> Optional[QUrl]:
    """
    弹出选择目录URL对话框，获取已存在的目录URL

    Args:
        parent: 父窗口
        title:  对话框标题
        start_dir: 起始目录
        supported_schemes: 支持的URL协议

    Returns:
        用户选择的目录URL，如果用户取消选择，则返回None
    """
    if start_dir is None:
        start_dir = QUrl()
    if not supported_schemes:
        url = QFileDialog.getExistingDirectoryUrl(
            parent,
            title,
            start_dir,
            QFileDialog.ShowDirsOnly,
        )
    else:
        url = QFileDialog.getExistingDirectoryUrl(
            parent,
            title,
            start_dir,
            QFileDialog.ShowDirsOnly,
            supportedSchemes=supported_schemes,
        )
    return url


def get_open_file(
    parent: Optional[QWidget] = None,
    title: str = "Open File",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    """
    弹出选择文件对话框，获取已存在的文件路径。

    Args:
        parent: 父窗口
        title:  对话框标题
        start_dir: 起始目录
        filters: 文件过滤器

    Returns:
        用户选择的文件路径，如果用户取消选择，则返回None。
    """
    filename, _ = compat.getopenfilename(parent, title, start_dir, filters)
    return filename or None


def get_open_files(
    parent: Optional[QWidget] = None,
    title: str = "Open Files",
    start_dir: str = "",
    filters: str = "",
) -> Optional[List[str]]:
    """
    弹出选择多个文件对话框，获取已存在的文件路径。

    Args:
        parent: 父窗口
        title:  对话框标题
        start_dir:  起始目录
        filters:  文件过滤器

    Returns:
        用户选择的文件路径列表，如果用户取消选择，则返回None。
    """
    filenames, _ = compat.getopenfilenames(parent, title, start_dir, filters)
    return filenames or None


def get_save_file(
    parent: Optional[QWidget] = None,
    title: str = "Save File",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    """
    弹出保存文件对话框，获取保存文件的路径。

    Args:
        parent: 父窗口
        title:  对话框标题
        start_dir: 起始目录
        filters: 文件过滤器

    Returns:
        用户选择的保存文件路径，如果用户取消选择，则返回None。
    """
    filename, _ = compat.getsavefilename(parent, title, start_dir, filters)
    return filename or None
