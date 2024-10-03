from pyguiadapter.adapter import GUIAdapter


def function_2(arg1: int, arg2: str, arg3: bool):
    """
    <h3>Description</h3>
    <p>
    This is the document of the <b>function_1</b>. And by default this document will automatically
    appear in the <strong>document area</strong>.
    </p>
    <p>
    The format of the document is <b>Markdown</b> by default. The <b>plaintext</b> and <b>html</b> formats are also
    supported.
    </p>
    <hr>
    <h3>Arguments</h3>
    <p>This function needs 3 arguments:</p>
    <ul>
    <li><b>arg1</b>: Balabala....</li>
    <li><b>arg2</b>: Balabala....</li>
    <li><b>arg3</b>: Balabala....</li>
    </ul>

    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(function_2, document_format="html")
    adapter.run()
