from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.widgets import IntSpinBoxConfig


def parameter_anchor_example(a: int, b: int, c: int, d: int, e: int, f: int):
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
    )
    adapter.run()
