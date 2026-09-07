"""Exact checks for the four-supporting-line orchard construction."""

from __future__ import annotations

from fractions import Fraction
from math import lcm


Point = tuple[Fraction, Fraction]


def ceil_half(value: int) -> int:
    """Return ceil(value / 2) using integer arithmetic."""

    return -((-value) // 2)


def parameters(n: int) -> tuple[int, int, int, int, int, int, int]:
    """Return (s, a, b, c, d, u, v) for the corrected construction."""

    if n < 28:
        raise ValueError("the stated construction is for n >= 28")
    s = 3 * (n + 1) // 7
    a = s // 2
    b = ceil_half(s)
    c = (n - s) // 2
    d = ceil_half(n - s)
    u = (s - c - 1) // 2
    v = ceil_half(s - d - 1)
    return s, a, b, c, d, u, v


def intervals(n: int) -> tuple[range, range, range, range]:
    """Return the four integer-index intervals A, B, C, and D."""

    _, a, b, c, d, u, v = parameters(n)
    return (
        range(a),
        range(b),
        range(u, u + c),
        range(-(b - 1) + v, -(b - 1) + v + d),
    )


def guaranteed_line_count(n: int) -> int:
    """Count admissible pairs (x,y), hence guaranteed four-point lines."""

    a_set, b_set, c_set, d_set = intervals(n)
    c_values = set(c_set)
    d_values = set(d_set)
    return sum(
        x + y in c_values and x - y in d_values
        for x in a_set
        for y in b_set
    )


def mistyped_line_count(n: int) -> int:
    """Count after the erroneous replacement v=ceil((s-c-1)/2)."""

    s, a, b, c, d, u, _ = parameters(n)
    wrong_v = ceil_half(s - c - 1)
    c_values = set(range(u, u + c))
    d_values = set(range(-(b - 1) + wrong_v, -(b - 1) + wrong_v + d))
    return sum(
        x + y in c_values and x - y in d_values
        for x in range(a)
        for y in range(b)
    )


def target_count(n: int) -> int:
    return (n * n + 12) // 28


def rational_points(n: int) -> tuple[list[Point], list[Point], list[Point], list[Point]]:
    """Return the four point families P, Q, R, and S."""

    a_set, b_set, c_set, d_set = intervals(n)
    p = [(Fraction(1, 3 * n + x), Fraction(0)) for x in a_set]
    q = [(Fraction(0), Fraction(1, n + y)) for y in b_set]
    r = [
        (Fraction(1, 4 * n + z), Fraction(1, 4 * n + z))
        for z in c_set
    ]
    s = [
        (Fraction(1, 2 * n + w), -Fraction(1, 2 * n + w))
        for w in d_set
    ]
    return p, q, r, s


def admissible_pairs(n: int):
    """Yield every (x,y) that produces a guaranteed four-point line."""

    a_set, b_set, c_set, d_set = intervals(n)
    c_values = set(c_set)
    d_values = set(d_set)
    for x in a_set:
        for y in b_set:
            if x + y in c_values and x - y in d_values:
                yield x, y


def line_value(n: int, x: int, y: int, point: Point) -> Fraction:
    """Evaluate the normalized line equation at a point."""

    coordinate_x, coordinate_y = point
    return (3 * n + x) * coordinate_x + (n + y) * coordinate_y


def integer_dilation(n: int) -> tuple[int, list[tuple[int, int]]]:
    """Dilate all rational points by a common denominator."""

    families = rational_points(n)
    points = [point for family in families for point in family]
    scale = lcm(*(coordinate.denominator for point in points for coordinate in point))
    integer_points = [
        (int(scale * coordinate_x), int(scale * coordinate_y))
        for coordinate_x, coordinate_y in points
    ]
    return scale, integer_points


if __name__ == "__main__":
    for n in (28, 29, 59, 60):
        print(n, guaranteed_line_count(n), target_count(n))
