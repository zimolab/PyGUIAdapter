import os
from typing import Optional, List

from PyQt6.QtWidgets import QTextEdit, QWidget, QMessageBox, QLayout, QFileDialog

from pyguiadapter.commons import DocumentFormat
from .styles import (
    DEFAULT_OUTPUT_BG_COLOR,
    DEFAULT_OUTPUT_TEXT_COLOR,
    DEFAULT_OUTPUT_FONT_FAMILY,
    DEFAULT_OUTPUT_FONT_SIZE,
    get_textedit_stylesheet,
)


def setup_textedit_stylesheet(
    textedit: QTextEdit,
    bg_color: str = DEFAULT_OUTPUT_BG_COLOR,
    text_color: str = DEFAULT_OUTPUT_TEXT_COLOR,
    font_family: str = DEFAULT_OUTPUT_FONT_FAMILY,
    font_size: int = DEFAULT_OUTPUT_FONT_SIZE,
):
    textedit.setStyleSheet(
        get_textedit_stylesheet(
            bg_color=bg_color,
            text_color=text_color,
            font_family=font_family,
            font_size=font_size,
        )
    )


def set_textedit_text(
    textedit: QTextEdit,
    text: str,
    text_format: DocumentFormat,
    goto_start: bool = False,
):
    if text_format == DocumentFormat.HTML:
        textedit.setHtml(text)
    elif text_format == DocumentFormat.MARKDOWN:
        textedit.setMarkdown(text)
    else:
        textedit.setPlainText("")
        textedit.append(text)
    # scroll to document start
    if goto_start:
        vb = textedit.verticalScrollBar()
        if vb:
            vb.setValue(0)


def show_info_dialog(parent: QWidget, message: str, *, title: str = None):
    QMessageBox.information(parent, title, message)


def show_warning_dialog(parent: QWidget, message: str, *, title: str = None):
    QMessageBox.warning(parent, title, message)


def show_critical_dialog(parent: QWidget, message: str, *, title: str = None):
    QMessageBox.critical(parent, title, message)


def show_question_dialog(parent: QWidget, message: str, *, title: str = None) -> bool:
    result = QMessageBox.question(
        parent,
        title,
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    return result == QMessageBox.StandardButton.Yes


def get_open_file_path(
    parent: QWidget,
    title: str = None,
    directory: str = None,
    filters: str = None,
    initial_filter: str = None,
) -> str:
    filepath, _ = QFileDialog.getOpenFileName(
        parent,
        title,
        directory,
        filters,
        initial_filter,
    )
    if not filepath:
        return ""
    return os.path.abspath(filepath)


def get_open_file_paths(
    parent: QWidget,
    title: str,
    directory: str = None,
    filters: str = None,
    initial_filter: str = None,
) -> Optional[List[str]]:
    ret, _ = QFileDialog.getOpenFileNames(
        parent,
        title,
        directory,
        filters,
        initial_filter,
    )
    if not ret:
        return None
    return [os.path.abspath(f) for f in ret]


def get_open_directory_path(
    parent: QWidget,
    title: str = None,
    directory: str = None,
) -> Optional[str]:
    directory = QFileDialog.getExistingDirectory(parent, title, directory)
    if not directory:
        return None
    return os.path.abspath(directory)


def get_save_file_path(
    parent: QWidget,
    title: str = None,
    directory: str = None,
    filters: str = None,
    initial_filter: str = None,
) -> Optional[str]:
    filepath, _ = QFileDialog.getSaveFileName(
        parent,
        title,
        directory,
        filters,
        initial_filter,
    )
    if not filepath:
        return None
    return os.path.abspath(filepath)


def clear_layout(layout: QLayout):
    if not layout:
        return
    while layout.count() > 0:
        item = layout.takeAt(0)

        widget = item.widget()
        if widget:
            widget.deleteLater()

        child_layout = item.layout()
        if child_layout:
            clear_layout(child_layout)
            continue

        spacer_item = item.spacerItem()
        if spacer_item:
            layout.removeItem(spacer_item)
