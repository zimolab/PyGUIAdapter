import math
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.adapter.uoutput import uprint


def solve(a: float, b: float, c: float) -> list:
    """
    Equation Solver, solving equations like:

    **ax^2 + bx + c = 0** (a,b,c ∈ R)
    """
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
