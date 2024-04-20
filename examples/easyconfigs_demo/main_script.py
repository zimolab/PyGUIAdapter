from PyQt6.QtCore import QDateTime, QDate, QTime
from PyQt6.QtGui import QColor
from function2widgets import Color
from datetime import date, datetime, time


def foo(
    a: int,
    b: float,
    c: bool,
    d: str,
    e: tuple,
    f: list,
    g: dict,
    color2: QColor,
    h: str = "12345",
    color: Color = Color(0, 0, 0),
    datetime1: datetime = datetime.now(),
    date1: date = date.today(),
    time1: time = time(0, 0, 0),
    datetime2: QDateTime = QDateTime.currentDateTime(),
    date2: QDate = QDate.currentDate(),
    time2: QTime = QTime.currentTime(),
):
    """
    Args:
        a: param a
        b: param b
        c: param c
        d: param d
        e: param e
        f: param f
        g: param g
        h: param h
        color: param color
        color2: param color2
        datetime1:
        datetime2:
        date1:
        date2:
        time1:
        time2:
    """


if __name__ == "__main__":
    from pyguiadapter import GUIAdapter

    # import generated configs file
    from examples.easyconfigs_demo._configs import CONFIGS

    gui_adapter = GUIAdapter()
    gui_adapter.add(foo, widget_configs=CONFIGS)
    gui_adapter.run()
