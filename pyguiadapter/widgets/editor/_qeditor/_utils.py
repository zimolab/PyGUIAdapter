import os.path

BASE_PATH = os.path.dirname(__file__)
RES_PATH = os.path.join(BASE_PATH, "resource")


def get_resource_path(filename: str) -> str:
    return os.path.join(RES_PATH, filename)


def read_resource_file(filename: str) -> bytes:
    res_path = get_resource_path(filename)
    with open(res_path, "rb") as f:
        return f.read()


def read_resource_text(filename: str, encoding: str = "utf-8") -> str:
    with open(get_resource_path(filename), "r", encoding=encoding) as f:
        return f.read()
