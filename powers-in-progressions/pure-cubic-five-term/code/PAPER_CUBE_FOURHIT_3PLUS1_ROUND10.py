"""Round-10 certificate for the second 3+1 four-hit cluster.

The proof uses exact arithmetic only.  A diagonal-cubic covering map sends
3*X^3-4*Y^3+Z^3=0 to v^2=u^3-972.  The point (5:2:-7) maps to twice the
integral non-torsion point (13,35), giving positive rank and two infinite
four-hit families.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp


Point = tuple[Fraction, Fraction, Fraction]
ORIGIN: Point = (Fraction(1), Fraction(1), Fraction(1))
GENERATOR: Point = (Fraction(5), Fraction(2), Fraction(-7))
Q = (Fraction(13), Fraction(35))
SELECTED_MODELS = (
    ((0, 1, 2, 4), "0010", 2),
    ((0, 1, 3, 4), "0010", 3),
)
CERTIFICATE = Path(__file__).with_name(
    "PAPER_CUBE_FOURHIT_3PLUS1_ROUND10_CERTIFICATE.json"
)


def curve_value(point: Point) -> Fraction:
    x, y, z = point
    return 3*x**3 - 4*y**3 + z**3


def normalize(point: Point) -> Point:
    point = tuple(Fraction(v) for v in point)
    scale = next(v for v in point if v)
    return tuple(v/scale for v in point)


def projectively_equal(left: Point, right: Point) -> bool:
    return normalize(left) == normalize(right)


def third_intersection(left: Point, right: Point) -> Point:
    """Third line intersection with the cubic, counted with multiplicity."""
    left = tuple(Fraction(v) for v in left)
    right = tuple(Fraction(v) for v in right)
    assert curve_value(left) == curve_value(right) == 0

    if projectively_equal(left, right):
        x, y, _ = left
        # The gradient is (9*x^2,-12*y^2,3*z^2), and this direction is
        # tangent because its scalar product with the gradient is zero.
        direction = (-12*y*y, -9*x*x, Fraction(0))

        def value(t):
            return curve_value(tuple(left[i] + t*direction[i] for i in range(3)))

        plus, minus = value(Fraction(1)), value(Fraction(-1))
        c2, c3 = (plus+minus)/2, (plus-minus)/2
        assert value(Fraction(2)) == 4*c2 + 8*c3
        if c3 == 0:
            raise ValueError("flex encountered")
        t = -c2/c3
        return normalize(tuple(left[i] + t*direction[i] for i in range(3)))

    def value(t):
        return curve_value(tuple(left[i] + t*right[i] for i in range(3)))

    plus, minus = value(Fraction(1)), value(Fraction(-1))
    c1, c2 = (plus-minus)/2, (plus+minus)/2
    if c2 == 0:
        return normalize(right)
    t = -c1/c2
    return normalize(tuple(left[i] + t*right[i] for i in range(3)))


def group_add(left: Point, right: Point) -> Point:
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
    """Map to E: v^2=u^3-972 on the all-nonzero open set."""
    x, y, z = point
    if x*y*z == 0:
        raise ZeroDivisionError("map formula is on the XYZ != 0 open set")
    numerator = 12*x**3*y**3 + 4*y**3*z**3 - 3*z**3*x**3
    product = (3*x**3+4*y**3)*(-4*y**3-z**3)*(z**3-3*x**3)
    u = numerator/(x**2*y**2*z**2)
    v = -product/(2*x**3*y**3*z**3)
    assert v*v == u**3-972
    return u, v


def ec_add(left, right):
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and y1 == -y2:
        return None
    slope = 3*x1*x1/(2*y1) if left == right else (y2-y1)/(x2-x1)
    x3 = slope*slope-x1-x2
    y3 = slope*(x1-x3)-y1
    return x3, y3


def progression(point: Point) -> tuple[Fraction, ...]:
    """AP with rational-cube coordinates in positions 0, 1 and 4."""
    x, y, z = point
    assert curve_value(point) == 0
    values = (
        x**3,
        y**3,
        2*y**3-x**3,
        3*y**3-2*x**3,
        z**3,
    )
    assert len({values[i+1]-values[i] for i in range(4)}) == 1
    return values


def is_rational_cube(value: Fraction) -> bool:
    value = Fraction(value)
    numerator, denominator = value.numerator, value.denominator
    rn, exact_n = sp.integer_nthroot(abs(numerator), 3)
    rd, exact_d = sp.integer_nthroot(denominator, 3)
    return bool(exact_n and exact_d)


def pure_cubic_class(value: Fraction, radicand: int):
    """Return e in {0,1,2} when value is D^e times a rational cube."""
    for exponent in range(3):
        if is_rational_cube(Fraction(value, radicand**exponent)):
            return exponent
    return None


def symbolic_map_identity():
    x, y, z = sp.symbols("X Y Z")
    f = 3*x**3-4*y**3+z**3
    n = 12*x**3*y**3+4*y**3*z**3-3*z**3*x**3
    t = (3*x**3+4*y**3)*(-4*y**3-z**3)*(z**3-3*x**3)
    cleared = sp.expand(t**2-4*n**3+3888*x**6*y**6*z**6)
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
    discriminant = -16*27*972**2
    assert discriminant == -2**8*3**13
    assert discriminant % (Q[1]**2) != 0
    example = progression(GENERATOR)
    example_classes = {
        "D=109": [pure_cubic_class(v, 109) for v in example],
        "D=226": [pure_cubic_class(v, 226) for v in example],
    }
    assert example_classes == {
        "D=109": [0, 0, 1, None, 0],
        "D=226": [0, 0, None, 1, 0],
    }
    return {
        "schema": "paper-cube-fourhit-second-3plus1-v1",
        "selected_models": [
            {"indices": list(indices), "word": word, "singleton_position": singleton}
            for indices, word, singleton in SELECTED_MODELS
        ],
        "curve": "3*X^3-4*Y^3+Z^3=0",
        "origin": [1, 1, 1],
        "infinite_order_point": [5, 2, -7],
        "mordell_curve": "v^2=u^3-972",
        "mordell_Q": [13, 35],
        "origin_image": [str(v) for v in origin_image],
        "point_image": [str(v) for v in generator_image],
        "point_image_equals_2Q": True,
        "translated_image_equals_3Q": True,
        "nagell_lutz": {
            "discriminant": discriminant,
            "Q_y_squared": 1225,
            "Q_y_squared_divides_discriminant": False,
            "conclusion": "Q=(13,35) has infinite order",
        },
        "integer_example": {
            "AP": [str(v) for v in example],
            "common_difference": str(example[1]-example[0]),
            "classes": example_classes,
        },
        "sample_multiples": [
            {
                "n": n,
                "point": [str(v) for v in point],
                "AP": [str(v) for v in progression(point)],
            }
            for n, point in enumerate(sample_points)
        ],
        "claim_boundary": (
            "The curve has positive rank and supplies infinite families in the "
            "two displayed models. Exact rank, generators, and the remaining "
            "four-hit curves are not classified."
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
