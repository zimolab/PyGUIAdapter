import math
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint
from pyguiadapter.exceptions import ParameterError


def solve(a: float, b: float, c: float) -> list:
    """A simple equation solver for equations like:

    **ax^2 + bx + c = 0** (a, b, c ∈ **R**, a != 0)

    @param a: parameter a, <span style="color:red;">a != 0</span>
    @param b: parameter b
    @param c: parameter c
    @return:

    @params

    [a]
    default_value = 1.0
    decimals = 5
    step = 0.00005

    [b]
    default_value = 1.0
    decimals = 5
    step = 0.00005

    [c]
    default_value = 0.0
    decimals = 5
    step = 0.00005

    @end

    """
    if a == 0:
        raise ParameterError(parameter_name="a", message="a cannot be zero")

    uprint("Solving Equation:")
    uprint(f"  {a}x² + {b}x + {c} = 0")
    discriminant = b**2 - 4 * a * c
    uprint(f"  Δ = {discriminant}", end="")
    if discriminant < 0:
        uprint(" < 0, no real roots")
        return []
    elif discriminant == 0:
        uprint(" = 0, one real root")
        return [-b / (2 * a)]
    else:
        uprint(" > 0, two real roots")
        sqrt_discriminant = math.sqrt(discriminant)
        return [(-b + sqrt_discriminant) / (2 * a), (-b - sqrt_discriminant) / (2 * a)]


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(solve)
    adapter.run()
