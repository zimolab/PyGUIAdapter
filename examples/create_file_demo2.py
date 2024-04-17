import os.path


def create_file(
    path: str,
    filename: str,
    content: str,
    overwrite: bool = True,
):
    """
    这是一个演示程序，用于演示<b>PyGUIAdapter</b>的功能，这段文字会被提取为函数的Document，并显示在界面上。

    :param path: <b>生成文件的保存的目录，若为空则保存到当前路径下</b>
    :param filename: <b>生成文件的文件名称。注意：<font color=red>不可为空！</font></b>
    :param content: <b>生成文件的内容</b>
    :param overwrite:
    :return:

    @widgets
    [path]
    widget_class="DirPathEdit"
    label="保存路径"
    button_text="选择目录"
    placeholder="选择文件保存的目录"

    [filename]
    label="文件名"
    placeholder="生成文件的名称"
    clear_button=true

    [content]
    widget_class="PlainTextEdit"
    label="文件内容"
    placeholder="生成文件的内容"

    [overwrite]
    label=""
    text="是否覆盖现有文件？"

    @end
    """
    if not path:
        path = "./"
    if not filename:
        raise ValueError("文件名不可为空，请指定文件名称")
    path = os.path.join(path, filename)
    if not os.path.isfile(path) or overwrite:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            return True
    return False


if __name__ == "__main__":
    from pyguiadapter import GUIAdapter

    gui_adapter = GUIAdapter()
    gui_adapter.add(create_file)
    gui_adapter.run()
