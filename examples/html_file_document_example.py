from pyguiadapter import utils
from pyguiadapter.adapter import GUIAdapter


def function_3(arg1: int, arg2: str, arg3: bool):
    """

    @param arg1:
    @param arg2:
    @param arg3:
    @return:
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    html_doc = utils.read_text_file("document.html")
    adapter.add(function_3, document=html_doc, document_format="html")
    adapter.run()
