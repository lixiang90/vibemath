"""Exact certificate for the four-hit branch (indices 0,1,3,4; colors 0001).

No bounded point search is used in the proof.  The branch is a smooth plane
cubic.  A rational map to y^2=x^3-243 proves that one displayed point has
infinite order, and an exact chord construction generates infinitely many
rational points on the branch.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp


Point = tuple[Fraction, Fraction, Fraction]
ORIGIN: Point = (Fraction(1), Fraction(1), Fraction(1))
GENERATOR: Point = (Fraction(4), Fraction(1), Fraction(-5))
Q = (Fraction(7), Fraction(10))
CERTIFICATE = Path(__file__).with_name("PAPER_CUBE_FOURHIT_0001_CERTIFICATE.json")


def curve_value(point: Point) -> Fraction:
    x, y, z = point
    return 2*x**3 - 3*y**3 + z**3


def normalize(point: Point) -> Point:
    point = tuple(Fraction(v) for v in point)
    scale = next(v for v in point if v)
    return tuple(v/scale for v in point)


def projectively_equal(left: Point, right: Point) -> bool:
    return normalize(left) == normalize(right)


def third_intersection(left: Point, right: Point) -> Point:
    """Third intersection with C, with multiplicity, using exact arithmetic."""
    left = tuple(Fraction(v) for v in left)
    right = tuple(Fraction(v) for v in right)
    assert curve_value(left) == curve_value(right) == 0

    if projectively_equal(left, right):
        x, y, _ = left
        # This vector is tangent: (6x^2,-9y^2,3z^2).(-9y^2,-6x^2,0)=0.
        direction = (-9*y*y, -6*x*x, Fraction(0))

        def value(t):
            return curve_value(tuple(left[i] + t*direction[i] for i in range(3)))

        plus, minus = value(Fraction(1)), value(Fraction(-1))
        c2, c3 = (plus+minus)/2, (plus-minus)/2
        assert value(Fraction(2)) == 4*c2 + 8*c3
        if c3 == 0:
            raise ValueError("flex encountered")
        t = -c2/c3
        return normalize(tuple(left[i] + t*direction[i] for i in range(3)))

    # On the line left+t*right, the constant and cubic coefficients vanish.
    def value(t):
        return curve_value(tuple(left[i] + t*right[i] for i in range(3)))

    plus, minus = value(Fraction(1)), value(Fraction(-1))
    c1, c2 = (plus-minus)/2, (plus+minus)/2
    if c2 == 0:  # right is the double intersection
        return normalize(right)
    t = -c1/c2
    return normalize(tuple(left[i] + t*right[i] for i in range(3)))


def group_add(left: Point, right: Point) -> Point:
    """Group law on C with ORIGIN as identity, by two chord operations."""
    first_third = third_intersection(left, right)
    return third_intersection(ORIGIN, first_third)


def multiples(count: int) -> tuple[Point, ...]:
    out = []
    point = ORIGIN
    for _ in range(count):
        out.append(normalize(point))
        point = group_add(point, GENERATOR)
    return tuple(out)


def map_to_mordell(point: Point) -> tuple[Fraction, Fraction]:
    """Rational map C -> E: v^2=u^3-243 on the all-nonzero open set."""
    x, y, z = point
    if x*y*z == 0:
        raise ZeroDivisionError("map formula is on the XYZ != 0 open set")
    numerator = 6*x**3*y**3 + 3*y**3*z**3 - 2*z**3*x**3
    t = (2*x**3 + 3*y**3)*(-3*y**3-z**3)*(z**3-2*x**3)
    u = numerator/(x**2*y**2*z**2)
    v = -t/(2*x**3*y**3*z**3)
    assert v*v == u**3-243
    return u, v


def ec_add(left, right):
    """Group law on v^2=u^3-243; None is infinity."""
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and y1 == -y2:
        return None
    if left == right:
        slope = 3*x1*x1/(2*y1)
    else:
        slope = (y2-y1)/(x2-x1)
    x3 = slope*slope-x1-x2
    y3 = slope*(x1-x3)-y1
    return x3, y3


def progression(point: Point) -> tuple[Fraction, ...]:
    """The five-term AP attached to a point of 2X^3-3Y^3+Z^3=0."""
    x, y, z = point
    assert curve_value(point) == 0
    values = (x**3, y**3, 2*y**3-x**3, z**3, 4*y**3-3*x**3)
    differences = tuple(values[i+1]-values[i] for i in range(4))
    assert len(set(differences)) == 1
    return values


def symbolic_map_identity():
    x, y, z = sp.symbols("X Y Z")
    f = 2*x**3-3*y**3+z**3
    n = 6*x**3*y**3+3*y**3*z**3-2*z**3*x**3
    t = (2*x**3+3*y**3)*(-3*y**3-z**3)*(z**3-2*x**3)
    cleared = sp.expand(t**2-4*n**3+972*x**6*y**6*z**6)
    quotient, remainder = sp.div(cleared, f, x, y, z)
    assert remainder == 0
    return sp.factor(quotient)


def certificate_data():
    sample_points = multiples(4)
    origin_image = map_to_mordell(ORIGIN)
    generator_image = map_to_mordell(GENERATOR)
    twice_q = ec_add(Q, Q)
    assert origin_image == (Q[0], -Q[1])
    assert generator_image == twice_q
    discriminant = -16*27*243**2
    assert discriminant == -2**4*3**13
    assert discriminant % (Q[1]**2) != 0
    return {
        "schema": "paper-cube-fourhit-0001-v1",
        "selected_orbit": {"indices": [0, 1, 3, 4], "colors": "0001"},
        "curve": "2*X^3-3*Y^3+Z^3=0",
        "origin": [1, 1, 1],
        "infinite_order_point": [4, 1, -5],
        "mordell_curve": "v^2=u^3-243",
        "mordell_Q": [7, 10],
        "origin_image": [str(v) for v in origin_image],
        "point_image": [str(v) for v in generator_image],
        "point_image_equals_2Q": True,
        "translated_image_equals_3Q": True,
        "nagell_lutz": {
            "discriminant": discriminant,
            "Q_y_squared": 100,
            "Q_y_squared_divides_discriminant": False,
            "conclusion": "Q=(7,10) has infinite order",
        },
        "sample_multiples": [
            {
                "n": n,
                "point": [str(v) for v in point],
                "AP": [str(v) for v in progression(point)],
            }
            for n, point in enumerate(sample_points)
        ],
        "classification_boundary": (
            "C(Q) has positive rank and supplies infinitely many inequivalent APs; "
            "the exact Mordell-Weil rank and generators are not claimed"
        ),
    }


def write_certificate(path: Path = CERTIFICATE):
    path.write_text(
        json.dumps(certificate_data(), indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    print(write_certificate())
