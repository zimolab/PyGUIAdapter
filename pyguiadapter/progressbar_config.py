import dataclasses


@dataclasses.dataclass
class ProgressBarConfig(object):
    min_value: int = 0
    max_value: int = 100
    inverted_appearance: bool = False
    show_progressbar_info: bool = True
    show_progress_text: bool = True
    progress_text_centered: bool = False
    progress_text_format: str = "%p%"
