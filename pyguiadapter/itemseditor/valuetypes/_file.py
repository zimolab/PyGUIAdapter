from ._path import *


class FileValue(PathValue):
    def __init__(
        self,
        default_value: str = "",
        *,
        display_name: Optional[str] = None,
        title: str = TITLE,
        any_file: bool = False,
        file_filters: str = FILE_FILTERS,
        selected_filter: str = SELECTED_FILTER,
        start_directory: str = START_DIRECTORY,
        as_posix: bool = AS_POSIX,
        readonly: bool = False,
        hidden: bool = False,
    ):
        if any_file:
            file_mode = "any_file"
        else:
            file_mode = "existing_file"

        # noinspection PyTypeChecker
        super().__init__(
            default_value or "",
            display_name=display_name,
            title=title,
            file_mode=file_mode,
            show_dirs_only=False,
            start_directory=start_directory,
            file_filters=file_filters,
            selected_filter=selected_filter,
            as_posix=as_posix,
            readonly=readonly,
            hidden=hidden,
        )
