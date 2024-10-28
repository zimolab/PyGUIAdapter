import os

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.utils import read_text_file
from pyguiadapter.windows import DocumentBrowserConfig
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig

DOCUMENT_PATH = os.path.join(os.path.dirname(__file__), "anchors_in_document.md")


def anchors_in_document(
    a: str,
    b: str,
    c: str,
    d: str,
    e: str,
    f: str,
    g: str,
    h: str,
    i: str,
    j: str,
    k: str,
    l: str,
    m: str,
    n: str,
    o: str,
    p: str,
):
    """
    This is an example demonstrating how to use parameter anchors and group anchors in the document of function.

    Args:
        a: description of parameter a.
        b: description of parameter b.
        c: description of parameter c.
        d: description of parameter d.
        e: description of parameter e.
        f: description of parameter f.
        g: description of parameter g.
        h: description of parameter h.
        i: description of parameter i.
        j: description of parameter j.
        k: description of parameter k.
        l: description of parameter l.
        m: description of parameter m.
        n: description of parameter n.
        o: description of parameter o.
        p: description of parameter p.
    """
    pass


if __name__ == "__main__":

    widget_configs = {
        # parameters in Group-A
        "a": {"group": "Group-A"},
        "b": {"group": "Group-A"},
        "c": {"group": "Group-A"},
        "d": {"group": "Group-A"},
        # parameters in Group-B
        "e": {"group": "Group-B"},
        "f": {"group": "Group-B"},
        "g": {"group": "Group-B"},
        "h": {"group": "Group-B"},
        # parameters in Group-C
        "i": {"group": "Group-C"},
        "j": {"group": "Group-C"},
        "k": {"group": "Group-C"},
        "l": {"group": "Group-C"},
        # parameters in default group
        "m": {"group": None},
        "n": {"group": None},
        "o": {"group": None},
        "p": {"group": None},
    }

    document = read_text_file(DOCUMENT_PATH)
    adapter = GUIAdapter()
    adapter.add(
        anchors_in_document,
        document=document,
        document_format="markdown",
        widget_configs=widget_configs,
        window_config=FnExecuteWindowConfig(
            document_browser_config=DocumentBrowserConfig(
                parameter_anchor=True, group_anchor=True
            )
        ),
    )
    adapter.run()
