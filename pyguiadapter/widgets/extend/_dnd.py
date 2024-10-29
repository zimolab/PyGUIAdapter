from pyguiadapter.utils import match_file_filters


def default_dnd_filter(filters: str, file_path: str) -> bool:
    if not filters:
        return True
    matched, filter_pattern = match_file_filters(filters, file_path)
    return matched
