from typing import List, Literal
from pyguiadapter.adapter import GUIAdapter


def process_integers(
    integers: List[int], operation: Literal["sum", "max"] = "max"
) -> int:
    """
    Process some integers.

    @param integers: an integer for the accumulator
    @param operation: sum the integers (default: find the max)
    """
    func = max if operation == "max" else sum
    return func(integers)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(process_integers)
    adapter.run()
