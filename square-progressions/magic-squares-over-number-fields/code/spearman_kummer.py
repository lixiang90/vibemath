"""Exact Kummer checks for Spearman's rank-three AP family.

Spearman's family is parametrized by a rational point (t, w) on

    w^2 = 9*t^4 + 4*t^2 + 36.

Writing t = u/v in lowest terms gives a congruent-number curve E_n and
three rational points whose x-coordinates are in arithmetic progression.
This module records the formulas from Theorem 1 of Spearman (2011) and
tests the extra ``point lies in 2E(Q)`` condition required by a magic
square of nine squares.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from fractions import Fraction

from magic_square_search import (
    Point,
    add_points,
    certified_center_progressions,
    is_rational_square,
    point_is_on_curve,
    search_curve,
)


@dataclass(frozen=True)
class SpearmanSpecialization:
    u: int
    v: int
    w: Fraction
    a: int
    b: int
    n: int
    points: tuple[Point, Point, Point]


@dataclass(frozen=True)
class SquarefreeModel:
    d: int
    scale_root: int
    points: tuple[Point, Point, Point]


def spearman_specialization(u: int, v: int, w: Fraction | int) -> SpearmanSpecialization:
    """Construct the curve and the three displayed AP points exactly."""
    if v == 0 or u == 0 or math.gcd(u, v) != 1:
        raise ValueError("Require nonzero coprime integers u and v")
    if v < 0:
        u, v = -u, -v
    w = Fraction(w)
    t = Fraction(u, v)
    if w * w != 9 * t**4 + 4 * t**2 + 36:
        raise ValueError("(u/v, w) is not on w^2 = 9t^4 + 4t^2 + 36")

    a = 3 * u**4 - 4 * u**2 * v**2 + 12 * v**4
    b = 3 * u**4 + 4 * u**2 * v**2 + 12 * v**4
    n = 6 * a * b
    points: tuple[Point, Point, Point] = (
        (
            Fraction(-18 * (u**2 - 2 * v**2) ** 2 * a),
            Fraction(144 * (-u**2 + 2 * v**2) * a**2 * u * v),
        ),
        (
            Fraction(-3 * a**2),
            Fraction(9 * a**2 * (u**2 + 2 * v**2) * w * v**2),
        ),
        (
            Fraction(-48 * u**2 * v**2 * a),
            Fraction(72 * u * v * a**2 * (u**2 + 2 * v**2)),
        ),
    )
    if not all(point_is_on_curve(point, n) for point in points):
        raise ArithmeticError("Transcribed Spearman point failed the curve equation")
    if points[0][0] - 2 * points[1][0] + points[2][0] != 0:
        raise ArithmeticError("Transcribed Spearman x-coordinates are not an AP")
    return SpearmanSpecialization(u, v, w, a, b, n, points)


def kummer_values(point: Point, n: int) -> tuple[Fraction, Fraction, Fraction]:
    """Return the three full-2-descent square tests for a non-torsion point."""
    if point is None:
        raise ValueError("The point at infinity needs a separate Kummer convention")
    x, _ = point
    return x - n, x, x + n


def is_double_point(point: Point, n: int) -> bool:
    """Test membership in 2E_n(Q) using the full rational 2-torsion."""
    return all(is_rational_square(value) for value in kummer_values(point, n))


def squarefree_part(value: int) -> int:
    """Canonical representative of an integral rational square class."""
    if value == 0:
        raise ValueError("Zero has no class in Q*/Q*2")
    sign = -1 if value < 0 else 1
    remainder = abs(value)
    if remainder.bit_length() > 40:
        # Trial division becomes unusable for later Spearman specializations.
        # SymPy's factorint uses Pollard rho/ECM as appropriate.
        from sympy import factorint

        factors = factorint(remainder)
        result = math.prod(prime for prime, exponent in factors.items() if exponent % 2)
        return sign * int(result)
    result = 1
    prime = 2
    while prime * prime <= remainder:
        parity = 0
        while remainder % prime == 0:
            remainder //= prime
            parity ^= 1
        if parity:
            result *= prime
        prime += 1 if prime == 2 else 2
    if remainder > 1:
        result *= remainder
    return sign * result


def squarefree_model(data: SpearmanSpecialization) -> SquarefreeModel:
    """Move E_n and its displayed points to the squarefree isomorphic model."""
    d = squarefree_part(data.n)
    quotient = data.n // d
    scale_root = math.isqrt(quotient)
    if scale_root * scale_root != quotient:
        raise ArithmeticError("Squarefree normalization did not leave a square quotient")
    x_scale = scale_root**2
    y_scale = scale_root**3
    points = tuple(
        (point[0] / x_scale, point[1] / y_scale) if point is not None else None
        for point in data.points
    )
    if not all(point_is_on_curve(point, d) for point in points):
        raise ArithmeticError("Squarefree model transformation failed")
    return SquarefreeModel(d, scale_root, points)


def alpha_x_class(point: Point) -> int:
    """The x-coordinate component of the 2-isogeny descent map."""
    if point is None or point[0].denominator != 1 or point[0] == 0:
        raise ValueError("This helper expects a nonzero integral x-coordinate")
    return squarefree_part(point[0].numerator)


def torsion_alpha_classes(n: int) -> frozenset[int]:
    """Alpha classes of O and the three rational points of order two."""
    n_class = squarefree_part(n)
    return frozenset((1, -1, n_class, -n_class))


def double_x(point: Point, n: int) -> Fraction:
    doubled = add_points(point, point, n)
    if doubled is None:
        raise ValueError("Cannot take the affine x-coordinate of this double")
    return doubled[0]


def doubled_ap_defect(data: SpearmanSpecialization) -> Fraction:
    """x(2P1) - 2*x(2P2) + x(2P3); zero would be an AP."""
    x1, x2, x3 = (double_x(point, data.n) for point in data.points)
    return x1 - 2 * x2 + x3


def doubled_ap_defect_formula(t: Fraction | int) -> Fraction:
    """Closed factorization of the doubled AP defect on Spearman's model."""
    t = Fraction(t)
    if t == 0:
        raise ValueError("Spearman's theorem excludes t=0")
    numerator = (
        (t**2 - 6) ** 2
        * (3 * t**2 - 2) ** 2
        * (3 * t**4 + 4 * t**2 + 12) ** 2
        * (9 * t**8 + 88 * t**4 + 144)
    )
    denominator = (
        8
        * t**2
        * (t**2 - 2) ** 2
        * (t**2 + 2) ** 2
        * (9 * t**4 + 4 * t**2 + 36)
    )
    # The displayed rational function is for the dehomogenized v=1 model.
    # Spearman's integral model has x-coordinates scaled by v^8.
    return t.denominator**8 * numerator / denominator


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--u", type=int, default=1)
    parser.add_argument("--v", type=int, default=1)
    parser.add_argument("--w", default="7", help="rational value, for example 818/27")
    parser.add_argument("--box", type=int, default=0, help="optional exact search box")
    args = parser.parse_args()

    data = spearman_specialization(args.u, args.v, Fraction(args.w))
    model = squarefree_model(data)
    t = Fraction(data.u, data.v)
    alpha = tuple(alpha_x_class(point) for point in data.points)
    torsion = torsion_alpha_classes(data.n)
    print(f"t={t}, w={data.w}, n={data.n}, squarefree D={model.d}, scale={model.scale_root}")
    print(f"x(P_i)={[point[0] for point in data.points]}")
    print(f"alpha(P_i)={alpha}; torsion alpha classes={sorted(torsion)}")
    print(f"P_i in 2E(Q)={[is_double_point(point, data.n) for point in data.points]}")
    defect = doubled_ap_defect(data)
    predicted = doubled_ap_defect_formula(t)
    print(f"doubled AP defect={defect}")
    print(f"factorized formula agrees={defect == predicted}; positive={defect > 0}")
    if args.box:
        centers, candidates = search_curve(
            model.d, model.points, box=args.box, minimum_squares=7
        )
        print(f"box={args.box}: centers={len(centers)}, seven-square candidates={len(candidates)}")
        print(f"fully certified center APs={len(certified_center_progressions(centers))}")


if __name__ == "__main__":
    main()
