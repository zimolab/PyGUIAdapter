from __future__ import annotations

from typing import List, Tuple, Set

from qtpy.QtWidgets import QLineEdit, QToolButton, QWidget, QHBoxLayout

from ... import utils


class PathSelectWidget(QWidget):

    DEFAULT_SELECT_BUTTON_TEXT = "..."
    DEFAULT_FILE_SEPARATOR = ";;"

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        select_directory: bool = False,
        open_file: bool = True,
        save_file: bool = False,
        multiple_files: bool = False,
        file_separator: str = DEFAULT_FILE_SEPARATOR,
        select_button_text: str | None = None,
        select_button_icon: utils.IconType = None,
        dialog_title: str = "",
        start_dir: str = "",
        filters: str | None = None,
        placeholder: str = "",
        clear_button: bool = False,
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

        self._path_edit = QLineEdit(self)
        if placeholder:
            self._path_edit.setPlaceholderText(placeholder)
        self._path_edit.setClearButtonEnabled(clear_button)

        self._select_button: QToolButton = QToolButton(self)

        if not select_button_text:
            select_button_text = self.DEFAULT_SELECT_BUTTON_TEXT
        self._select_button.setText(select_button_text)

        select_button_icon = utils.get_icon(select_button_icon)
        if select_button_icon:
            self._select_button.setIcon(select_button_icon)

        # noinspection PyUnresolvedReferences
        self._select_button.clicked.connect(self._on_select_path)

        self._layout.addWidget(self._path_edit)
        self._layout.addWidget(self._select_button)

    def _on_select_path(self):
        if self._select_directory:
            directory = utils.get_existing_directory(
                self, title=self._dialog_title or "", start_dir=self._start_dir or ""
            )
            if directory:
                self._path_edit.setText(directory)
            return

        if self._save_file:
            filename = utils.get_save_file(
                self,
                title=self._dialog_title or "",
                start_dir=self._start_dir or "",
                filters=self._filters or "",
            )
            if filename:
                self._path_edit.setText(filename)
            return

        if self._multiple_files:
            assert (
                self._file_separator is not None and self._file_separator.strip() != ""
            )
            filenames = utils.get_open_files(
                self,
                title=self._dialog_title or "",
                start_dir=self._start_dir or "",
                filters=self._filters or "",
            )
            if filenames:
                self._path_edit.setText(self._file_separator.join(filenames))
        else:
            filename = utils.get_open_file(
                self,
                title=self._dialog_title or "",
                start_dir=self._start_dir or "",
                filters=self._filters or "",
            )
            if filename:
                self._path_edit.setText(filename)

    def set_path(self, p: str):
        self._path_edit.setText(p)

    def get_path(self) -> str:
        return self._path_edit.text()

    def set_paths(self, ps: str | List[str] | Tuple[str, ...] | Set[str]):
        assert self._file_separator is not None and self._file_separator.strip() != ""
        if not isinstance(ps, str):
            ps = self._file_separator.join(ps)
        self._path_edit.setText(ps)

    def get_paths(self) -> List[str]:
        if not self._file_separator:
            return [self.get_path()]
        return self._path_edit.text().split(self._file_separator)
