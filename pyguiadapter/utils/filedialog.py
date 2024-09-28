from typing import List, Optional

from qtpy import compat
from qtpy.QtCore import QUrl
from qtpy.QtWidgets import QWidget, QFileDialog


def get_existing_directory(
    parent: Optional[QWidget] = None,
    title: str = "Open Directory",
    start_dir: str = "",
) -> str:
    return compat.getexistingdirectory(parent, title, start_dir)
    # return QFileDialog.getExistingDirectory(parent, title, start_dir)


def get_existing_directory_url(
    parent: Optional[QWidget] = None,
    title: str = "Open Directory URL",
    start_dir: Optional[QUrl] = None,
    supported_schemes: Optional[List[str]] = None,
) -> Optional[QUrl]:
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
    # filename, _ = QFileDialog.getOpenFileName(parent, title, start_dir, filters)
    filename, _ = compat.getopenfilename(parent, title, start_dir, filters)
    return filename or None


def get_open_files(
    parent: Optional[QWidget] = None,
    title: str = "Open Files",
    start_dir: str = "",
    filters: str = "",
) -> Optional[List[str]]:
    # filenames, _ = QFileDialog.getOpenFileNames(parent, title, start_dir, filters)
    filenames, _ = compat.getopenfilenames(parent, title, start_dir, filters)
    return filenames or None


def get_save_file(
    parent: Optional[QWidget] = None,
    title: str = "Save File",
    start_dir: str = "",
    filters: str = "",
) -> Optional[str]:
    # filename, _ = QFileDialog.getSaveFileName(parent, title, start_dir, filters)
    filename, _ = compat.getsavefilename(parent, title, start_dir, filters)
    return filename or None
