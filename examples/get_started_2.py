from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.types import file_t, directory_t


def encode_mp3(
    input_file: file_t, output_dir: directory_t, output_file: str, quality: int
):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(encode_mp3)
    adapter.run()
