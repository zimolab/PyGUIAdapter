"""
@Time    : 2024.10.20
@File    : io.py
@Author  : zimolab
@Project : PyGUIAdapter
@Desc    : 读写文件相关的工具函数
"""


def read_text_file(text_file: str, encoding: str = "utf-8") -> str:
    """
    读取文本文件内容。

    Args:
        text_file: 文件路径
        encoding: 文件编码，默认utf-8

    Returns:
        返回文件内容。
    """
    with open(text_file, "r", encoding=encoding) as f:
        return f.read()


def write_text_file(text_file: str, content: str, encoding: str = "utf-8") -> None:
    """
    写入文本文件内容。

    Args:
        text_file: 文件路径
        content:  文件内容
        encoding:  文件编码，默认utf-8

    Returns:
        无返回值
    """
    with open(text_file, "w", encoding=encoding) as f:
        f.write(content)


def read_file(file_path: str) -> bytes:
    """
    读取文件内容（以字节的方式）

    Args:
        file_path: 文件路径

    Returns:
        返回文件内容（以字节的方式）
    """
    with open(file_path, "rb") as f:
        return f.read()


def write_file(file_path: str, content: bytes) -> None:
    """
    写入文件内容（以字节的方式）
    Args:
        file_path: 文件路径
        content:  文件内容

    Returns:
        无返回值
    """
    with open(file_path, "wb") as f:
        f.write(content)
