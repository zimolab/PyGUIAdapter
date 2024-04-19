from PyQt6.QtCore import QDateTime, QDate, QTime
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
    this is a func doc

    line2

    :param a: param a
    2nd line

    """


if __name__ == "__main__":
    from pyguiadapter.tools.easyconfigs import FuncConfigsGenerator

    configs_generator = FuncConfigsGenerator()
    configs_generator.generate_configs_file(
        foo,
        onefile=False,
        constants_filename="_constants.py",
    )
