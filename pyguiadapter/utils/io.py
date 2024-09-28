def read_text_file(text_file: str, encoding: str = "utf-8") -> str:
    with open(text_file, "r", encoding=encoding) as f:
        return f.read()


def write_text_file(text_file: str, content: str, encoding: str = "utf-8"):
    with open(text_file, "w", encoding=encoding) as f:
        f.write(content)
