"""Exact j=1728 intersections in Bremner's long-AP families.

The formulas are from Andrew Bremner, "On Arithmetic Progressions on
Elliptic Curves", Experimental Mathematics 8 (1999), 409-413.
"""

from __future__ import annotations

from sympy import Poly, expand, factor, rem, resultant, symbols


r, z = symbols("r z")

# Equations (17) and (18), with the paper's homogeneous parameters x:y
# dehomogenized to r:1.
PRIMARY_D = factor(6 * r * (r - 1) * (r - 2))
PRIMARY_A = factor(-252 * r**2 * (r - 1) ** 2 * (r - 2) ** 2)
PRIMARY_B = factor(
    324 * r**2 * (r - 1) ** 2 * (r - 2) ** 2 * (r**2 - 2 * r + 2) ** 2
)
PRIMARY_J1728 = Poly(r**2 - 2 * r + 2, r, domain="QQ")

# Equations (21) and (22): either expression must be a square to extend
# the seven-term progression to length eight.
EIGHTH_POINT_1 = r**4 + 20 * r**3 - 64 * r**2 + 40 * r + 4
EIGHTH_POINT_2 = r**4 - 28 * r**3 + 80 * r**2 - 56 * r + 4

# The degree-24 factor in B for the second seven-term family on page 412.
SECOND_J1728 = Poly(
    3188646 * r**24
    + 183524292 * r**22
    + 2098837656 * r**20
    - 6763196898 * r**18
    + 4628564613 * r**16
    - 11781396216 * r**14
    + 68063427684 * r**12
    - 146498139396 * r**10
    + 163046846764 * r**8
    - 105881078940 * r**6
    + 40866792460 * r**4
    - 8775138762 * r**2
    + 815730721,
    r,
    domain="QQ",
)


def eighth_point_polynomial(expression) -> Poly:
    """Eliminate r on the primary j=1728 locus from z^2=expression."""
    value = resultant(PRIMARY_J1728.as_expr(), z**2 - expression, r)
    _, primitive = Poly(value, z, domain="QQ").primitive()
    return primitive


def primary_specialization_remainders() -> dict[str, object]:
    """Reduce the main coefficients modulo r^2-2r+2."""
    modulus = PRIMARY_J1728.as_expr()
    return {
        "d": expand(rem(PRIMARY_D, modulus, r)),
        "A": expand(rem(PRIMARY_A, modulus, r)),
        "B": expand(rem(PRIMARY_B, modulus, r)),
        "eighth_1": expand(rem(EIGHTH_POINT_1, modulus, r)),
        "eighth_2": expand(rem(EIGHTH_POINT_2, modulus, r)),
    }


def main() -> None:
    data = primary_specialization_remainders()
    print(f"primary B factorization: {PRIMARY_B}")
    print(f"nondegenerate j=1728 parameter: {PRIMARY_J1728.as_expr()}")
    print(f"irreducible degree: {PRIMARY_J1728.degree()}")
    print(f"remainders: {data}")
    for index, expression in enumerate((EIGHTH_POINT_1, EIGHTH_POINT_2), 1):
        polynomial = eighth_point_polynomial(expression)
        print(
            f"eighth branch {index}: {polynomial.as_expr()}, "
            f"degree={polynomial.degree()}, irreducible={polynomial.is_irreducible}"
        )
    print(
        f"second family j=1728 factor: degree={SECOND_J1728.degree()}, "
        f"irreducible={SECOND_J1728.is_irreducible}"
    )


if __name__ == "__main__":
    main()
