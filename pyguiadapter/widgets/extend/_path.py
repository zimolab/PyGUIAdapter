import os
from typing import List, Tuple, Set, Optional, Union

from qtpy.QtWidgets import QLineEdit, QToolButton, QWidget, QHBoxLayout

from ...utils import IconType, filedialog, get_icon

DEFAULT_SELECT_BUTTON_TEXT = "..."
DEFAULT_FILE_SEPARATOR = ";;"


class PathSelectWidget(QWidget):

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        select_directory: bool = False,
        open_file: bool = True,
        save_file: bool = False,
        multiple_files: bool = False,
        file_separator: str = DEFAULT_FILE_SEPARATOR,
        select_button_text: Optional[str] = None,
        select_button_icon: IconType = None,
        dialog_title: str = "",
        start_dir: str = "",
        filters: Optional[str] = None,
        placeholder: str = "",
        clear_button: bool = False,
        normalize_path: bool = False,
        absolutize_path: bool = False,
    ):
        super().__init__(parent)

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0, 0, 0, 0)
        # self._layout.setSpacing(0)

        self._select_directory = select_directory
        self._open_file = open_file
        self._save_file = save_file
        self._multiple_files = multiple_files
        self._file_separator = file_separator
        self._dialog_title = dialog_title
        self._start_dir = start_dir
        self._filters = filters
        self._normalize_path = normalize_path
        self._absolutize_path = absolutize_path

        self._path_edit = QLineEdit(self)
        if placeholder:
            self._path_edit.setPlaceholderText(placeholder)
        self._path_edit.setClearButtonEnabled(clear_button)

        self._select_button: QToolButton = QToolButton(self)

        if not select_button_text:
            select_button_text = self.DEFAULT_SELECT_BUTTON_TEXT
        self._select_button.setText(select_button_text)

        select_button_icon = get_icon(select_button_icon)
        if select_button_icon:
            self._select_button.setIcon(select_button_icon)

        # noinspection PyUnresolvedReferences
        self._select_button.clicked.connect(self._on_select_path)

        self._layout.addWidget(self._path_edit)
        self._layout.addWidget(self._select_button)

    def _norm_path(self, p: str) -> str:
        if p.strip() == "":
            return p
        if self._normalize_path:
            p = os.path.normpath(p)
        if self._absolutize_path:
            p = os.path.abspath(p)
        return p

    def _on_select_path(self):
        if self._select_directory:
            directory = filedialog.get_existing_directory(
                self, title=self._dialog_title or "", start_dir=self._start_dir or ""
            )
            if directory:
                self.set_path(directory)
        elif self._save_file:
            filename = filedialog.get_save_file(
                self,
                title=self._dialog_title or "",
                start_dir=self._start_dir or "",
                filters=self._filters or "",
            )
            if filename:
                self.set_path(filename)
        elif self._multiple_files:
            assert (
                self._file_separator is not None and self._file_separator.strip() != ""
            )
            filenames = filedialog.get_open_files(
                self,
                title=self._dialog_title or "",
                start_dir=self._start_dir or "",
                filters=self._filters or "",
            )
            if filenames:
                self.set_paths(filenames)
        else:
            filename = filedialog.get_open_file(
                self,
                title=self._dialog_title or "",
                start_dir=self._start_dir or "",
                filters=self._filters or "",
            )
            if filename:
                self.set_path(filename)

    def set_path(self, p: str):
        self._path_edit.setText(self._norm_path(p))

    def get_path(self) -> str:
        p = self._path_edit.text()
        return self._norm_path(p)

    def set_paths(self, ps: Union[str, List[str], Tuple[str, ...], Set[str]]):
        assert self._file_separator is not None and self._file_separator.strip() != ""
        if isinstance(ps, str):
            ps = [ps]

        if not self._file_separator:
            self.set_path(ps[0])
            return

        ps = self._file_separator.join(self._norm_path(p) for p in ps)
        self._path_edit.setText(ps)

    def get_paths(self) -> List[str]:
        if not self._file_separator:
            return [self.get_path()]
        return [
            self._norm_path(p)
            for p in self._path_edit.text().split(self._file_separator)
        ]
