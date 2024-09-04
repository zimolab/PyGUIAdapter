from pyguiadapter.adapter import GUIAdapter


def encode_mp3(input_file: str, output_dir: str, output_file: str, quality: int):
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(encode_mp3)
    adapter.run()
