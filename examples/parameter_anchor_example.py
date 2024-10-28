from datetime import datetime, date, time

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.extend_types import string_list_t
from pyguiadapter.widgets import IntSpinBoxConfig
from pyguiadapter.windows import DocumentBrowserConfig
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig


def parameter_anchor_example(
    a: int,
    b: float,
    c: bool,
    d: str,
    e: datetime,
    f: date,
    h: time,
    i: list,
    j: tuple,
    k: dict,
    l: string_list_t,
):
    """
    This example show how to use parameter anchor.
    <br>
    <h3>Parameter Anchors</h3>
    <a href="#param=a">click to jump to parameter a.</a>
    <br>
    <a href="#param=b">click to jump to parameter b.</a>
    <br>
    <a href="#param=c">click to jump to parameter c.</a>
    <br>
    <a href="#param=d">click to jump to parameter d.</a>
    <br>
    <a href="#param=e">click to jump to parameter e.</a>
    <br>
    <a href="#param=f">click to jump to parameter f.</a>
    <br>
    <a href="#param=h">click to jump to parameter h.</a>
    <br>
    <a href="#param=i">click to jump to parameter i.</a>
    <br>
    <a href="#param=j">click to jump to parameter j.</a>
    <br>
    <a href="#param=k">click to jump to parameter k.</a>
    <br>
    <a href="#param=l">click to jump to parameter l.</a>
    <h3>Group Anchors</h3>
    <a href="#group=">click to jump to default group</a>
    <br>
    <a href="#group=Group A">click to jump to group Group A.</a>
    <br>
    <a href="#group=Group B">click to jump to group Group B.</a>
    <br>
    <a href="#group=Group C">click to jump to group Group C.</a>

    Args:
        a: description of a.
        b: description of b.
        c: description of c.
        d: description of d.
        e: description of e.
        f: description of f.
        l: description of l.
        k: description of k.
        j: description of j.
        i: description of i.
        h: description of h.
    Returns:
    """
    pass


if __name__ == "__main__":
    a_conf = IntSpinBoxConfig(group="Group A")
    b_conf = IntSpinBoxConfig(group="Group B")
    c_conf = IntSpinBoxConfig(group="Group C")
    adapter = GUIAdapter()
    adapter.add(
        parameter_anchor_example,
        document_format="html",
        widget_configs={"a": a_conf, "b": b_conf, "c": c_conf},
        window_config=FnExecuteWindowConfig(
            document_browser_config=DocumentBrowserConfig(
                parameter_anchor=True, group_anchor=True
            )
        ),
    )
    adapter.run()
