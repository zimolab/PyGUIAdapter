from pyguiadapter.adapter import GUIAdapter


def function_1(arg1: int, arg2: str, arg3: bool):
    """
    ### Description
    This is the document of the **function_1**. And by default this document will automatically
    appear in the `document area`.

    The format of the document is **Markdown** by default. The **plaintext** and **html** formats are also
    supported.

    ---

    ### Arguments
    This function needs 3 arguments:
    - **arg1**: Balabala....
    - **arg2**: Balabala....
    - **arg3**: Balabala....

    @param arg1:
    @param arg2:
    @param arg3:
    @return:
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(function_1)
    adapter.run()
