import math
from pyguiadapter.adapter import GUIAdapter


def roots(a: float, b: float, c: float) -> list:
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return []
    elif discriminant == 0:
        return [-b / (2 * a)]
    else:
        sqrt_discriminant = math.sqrt(discriminant)
        return [(-b + sqrt_discriminant) / (2 * a), (-b - sqrt_discriminant) / (2 * a)]


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(roots)
    adapter.run()
