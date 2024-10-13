def read_text_file(text_file: str, encoding: str = "utf-8") -> str:
    with open(text_file, "r", encoding=encoding) as f:
        return f.read()


def write_text_file(text_file: str, content: str, encoding: str = "utf-8"):
    with open(text_file, "w", encoding=encoding) as f:
        f.write(content)


def read_file(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


def write_file(file_path: str, content: bytes):
    with open(file_path, "wb") as f:
        f.write(content)
