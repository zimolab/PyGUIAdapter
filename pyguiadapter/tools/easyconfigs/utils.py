import importlib.resources
import os.path

from .constants import TPL_DIR, TPL_PKG, TPL_FILENAME_CONFIGS, TPL_FILENAME_CONSTANTS


def get_tpl_dir() -> str:
    with importlib.resources.path(TPL_PKG, TPL_DIR) as tpl_dir:
        return str(tpl_dir)


def get_configs_tpl_file() -> str:
    return os.path.join(get_tpl_dir(), TPL_FILENAME_CONFIGS)


def get_constants_tpl_file() -> str:
    return os.path.join(get_tpl_dir(), TPL_FILENAME_CONSTANTS)


def write_text_blocks(filepath: str, block: str, *more_blocks: str):
    with open(filepath, "w", encoding="utf-8") as out_file:
        out_file.write(block)
        for block in more_blocks:
            out_file.write("\n")
            out_file.write(block)
        out_file.flush()
