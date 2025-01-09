from ._path import *


class DirectoryValue(PathValue):
    def __init__(
        self,
        default_value: str = "",
        *,
        display_name: Optional[str] = None,
        title: str = TITLE,
        show_dirs_only: bool = SHOW_DIRS_ONLY,
        start_directory: str = START_DIRECTORY,
        as_posix: bool = AS_POSIX,
        readonly: bool = False,
        hidden: bool = False,
    ):
        super().__init__(
            default_value or "",
            display_name=display_name,
            title=title,
            file_mode="directory",
            show_dirs_only=show_dirs_only,
            start_directory=start_directory,
            file_filters="",
            selected_filter="",
            as_posix=as_posix,
            readonly=readonly,
            hidden=hidden,
        )
