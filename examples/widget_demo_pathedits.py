"""
This demo shows widgets for selecting and editing paths, see: function2widgets.widgets.pathedit
"""

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.interact.uprint import uprint


def pathedits_demo(
    open_file_path: str,
    save_file_path: str,
    files_path: str,
    dir_path: str,
    save_dir_path: str,
):
    """
    This demo shows widgets for selecting and editing paths

    :param open_file_path:  get open file path
    :param save_file_path:  get save file path
    :param files_path:  get multiple files path
    :param dir_path:  get open directory path
    :param save_dir_path: get save directory path
    :return:

    @begin
    [open_file_path]
    type="FilePathEdit"
    select_button_text="open"
    save_file=false
    multiple_files=false
    filters="PY Files(*.py);;Text Files(*.txt);;All Files(*.*)"
    init_filter="Text Files(*.txt)"
    start_path="./"
    #path_delimiter=";"
    placeholder="select file path"
    clear_button=true
    dialog_title="Select File"

    [save_file_path]
    type="FilePathEdit"
    select_button_text="open"
    save_file=true
    #multiple_files=false
    filters="PY Files(*.py);;Text Files(*.txt);;All Files(*.*)"
    init_filter="Text Files(*.txt)"
    start_path="./"
    #path_delimiter=";"
    placeholder="select save file path"
    clear_button=true
    dialog_title="Save File"

    [files_path]
    type="FilePathEdit"
    select_button_text="open"
    save_file=false
    multiple_files=true
    filters="PY Files(*.py);;Text Files(*.txt);;All Files(*.*)"
    init_filter="Text Files(*.txt)"
    start_path="./"
    path_delimiter=";"
    placeholder="select files path"
    clear_button=true
    dialog_title="Open Files"

    [dir_path]
    type="DirPathEdit"
    select_button_text="open dir"
    save_dir=false
    start_path="./"
    placeholder="select dir path"
    clear_button=true
    dialog_title="Open Dir"

    [save_dir_path]
    type="DirPathEdit"
    select_button_text="open dir"
    save_dir=true
    start_path="./"
    placeholder="select save dir path"
    clear_button=true
    dialog_title="Save Dir"

    @end
    """
    uprint("open_file_path:", open_file_path)
    uprint("save_file_path:", save_file_path)
    uprint("files_path:", files_path)
    uprint("dir_path:", dir_path)
    uprint("save_dir_path:", save_dir_path)


gui_adapter = GUIAdapter()
gui_adapter.add(pathedits_demo)
gui_adapter.run()
