from typing import Literal

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint


def temperature_converter(
    temperature: float,
    from_unit: Literal["°C", "°F"] = "°F",
    to_unit: Literal["°C", "°F"] = "°C",
) -> float:
    """
    Convert temperature from one unit to another.
    ---
    *This is a simple demo of [`PyGUIAdapter`](https://github.com/zimolab/PyGUIAdapter).*

    Args:
        temperature (flot): current value of temperature
        from_unit (str): current unit of temperature
        to_unit (str):  target unit of temperature

    Returns:
        the converted value of temperature
    """
    if from_unit == "°C" and to_unit == "°F":
        converted = temperature * 9 / 5 + 32
    elif from_unit == "°F" and to_unit == "°C":
        converted = (temperature - 32) * 5 / 9
    else:
        converted = temperature
    uprint(f"{temperature}{from_unit} = {converted}{to_unit}")
    return converted


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(temperature_converter)
    adapter.run()
