from datetime import date

from pyguiadapter.adapter import GUIAdapter


def date_example(arg1: date, arg2: date, arg3: date):
    """
    example for type **date** and **DateEdit** widget
    """
    pass


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(date_example)
    adapter.run()
