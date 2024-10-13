from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import print_image
from pyguiadapter.extend_types import file_t


def print_image_example(
    image_path: file_t,
    image_type: str = "jpeg",
    width: int = None,
    height: int = None,
    embed_base64: bool = True,
    centered: bool = True,
):
    print_image(
        image_path,
        image_type,
        width=width,
        height=height,
        embed_base64=embed_base64,
        centered=centered,
    )


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(print_image_example)
    adapter.run()
