import os.path


def create_file(path: str, filename: str, content: str, overwrite: bool = False):
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
