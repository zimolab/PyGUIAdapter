from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter import ubeep


def beep_example(beep: bool):
    if beep:
        ubeep.beep()


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(beep_example)
    adapter.run()
