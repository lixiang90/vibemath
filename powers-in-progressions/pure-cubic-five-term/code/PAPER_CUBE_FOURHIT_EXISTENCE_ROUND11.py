"""Round-11 existence closure for the four-hit model 0102 on 0124.

This module contains exact identities only. It proves one nonconstant,
nonzero four-hit arithmetic progression over Q(cuberoot(6)) and proves that
its image on the natural elliptic quotient is non-torsion. It does *not*
claim that the genus-four source curve has infinitely many rational points.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "PAPER_CUBE_FOURHIT_EXISTENCE_ROUND11_CERTIFICATE.json"

INDICES = (0, 1, 2, 4)
CANONICAL_WORD = "0102"
CURVE_COEFFICIENTS = (-2, 2, 4, -4)
SOURCE_POINT = (Fraction(2), Fraction(1), Fraction(-3))
RADICAND = 6
INTEGER_AP = (64, 36, 8, -20, -48)
ELLIPTIC_POINT = (6, 15)


def source_value(point=SOURCE_POINT):
    """Evaluate -2 X^6+2 X^3 Y^3+4 Y^6-4 W^3."""
    X, Y, W = map(Fraction, point)
    a, b, c, w = CURVE_COEFFICIENTS
    return a * X**6 + b * X**3 * Y**3 + c * Y**6 + w * W**3


def factorized_source_value(point=SOURCE_POINT):
    """Evaluate (X^3+Y^3)(2Y^3-X^3)-2W^3."""
    X, Y, W = map(Fraction, point)
    return (X**3 + Y**3) * (2 * Y**3 - X**3) - 2 * W**3


def rational_progression(point=SOURCE_POINT):
    """Recover the AP from A_0=X^3 and A_2=Y^3."""
    X, Y, _ = map(Fraction, point)
    return tuple(Fraction((2 - k) * X**3 + k * Y**3, 2) for k in range(5))


def cube_class_mod_six(value):
    """Return c in {0,1,2} with value in 6^c Q^3, or None."""
    value = Fraction(value)
    if value == 0:
        return None
    for c in range(3):
        quotient = value / (RADICAND**c)
        numerator_root, numerator_exact = sp.integer_nthroot(
            abs(quotient.numerator), 3
        )
        denominator_root, denominator_exact = sp.integer_nthroot(
            quotient.denominator, 3
        )
        if numerator_exact and denominator_exact:
            assert numerator_root**3 == abs(quotient.numerator)
            assert denominator_root**3 == quotient.denominator
            return c
    return None


def raw_and_canonical_colors():
    raw = tuple(cube_class_mod_six(INTEGER_AP[k]) for k in INDICES)
    assert raw == (0, 2, 0, 1)
    canonical = tuple((2 * c) % 3 for c in raw)
    assert canonical == tuple(map(int, CANONICAL_WORD))
    return raw, canonical


def quotient_map(point=SOURCE_POINT):
    """Map the Y != 0 source chart to E: v^2=u^3+9.

    Completing the square in T=(X/Y)^3 gives
    (2T-1)^2=(-2W/Y^2)^3+9.
    """
    X, Y, W = map(Fraction, point)
    if Y == 0:
        raise ZeroDivisionError("the displayed quotient chart has Y != 0")
    u = -2 * W / Y**2
    v = 2 * (X / Y) ** 3 - 1
    assert v**2 == u**3 + 9
    return u, v


def nagell_lutz_nontorsion(point=ELLIPTIC_POINT):
    """Certify non-torsion on y^2=x^3+9 by Nagell--Lutz."""
    x, y = map(int, point)
    discriminant = -16 * 27 * 9**2
    assert y != 0
    assert y * y == x**3 + 9
    assert discriminant % (y * y) != 0
    return {
        "curve": "v^2=u^3+9",
        "point": [x, y],
        "discriminant": discriminant,
        "y_squared": y * y,
        "y_squared_divides_discriminant": False,
        "conclusion": "non-torsion by Nagell--Lutz",
    }


def field_and_hit_certificate():
    """Return explicit cube witnesses and the strict fifth-term exclusion."""
    ap = tuple(8 * value for value in rational_progression())
    assert ap == INTEGER_AP
    assert len(set(ap)) == 5 and all(ap)
    witnesses = {
        "A0": "4",
        "A1": "alpha^2",
        "A2": "2",
        "A4": "-2*alpha",
    }
    assert (4**3, RADICAND**2, 2**3, (-2) ** 3 * RADICAND) == (
        ap[0],
        ap[1],
        ap[2],
        ap[4],
    )
    assert cube_class_mod_six(ap[3]) is None
    omitted_v5_mod_3 = 1
    # x^3-6 is Eisenstein at 2, so the field really has degree three.
    return {
        "field": "Q(alpha), alpha^3=6",
        "degree": 3,
        "degree_proof": "x^3-6 is Eisenstein at 2",
        "integer_AP": [int(value) for value in ap],
        "common_difference": int(ap[1] - ap[0]),
        "cube_witnesses": witnesses,
        "omitted_index": 3,
        "omitted_value": int(ap[3]),
        "omitted_v5_mod_3": omitted_v5_mod_3,
        "omitted_exclusion": (
            "the Kummer kernel is <6> in Q*/Q*^3; its classes have "
            "v_5=0 mod 3, but v_5(-20)=1"
        ),
    }


def certificate_data():
    assert source_value() == 0
    assert factorized_source_value() == 0
    raw, canonical = raw_and_canonical_colors()
    assert quotient_map() == tuple(map(Fraction, ELLIPTIC_POINT))
    return {
        "schema": "paper-cube-fourhit-existence-round11-v1",
        "model": {"indices": list(INDICES), "canonical_word": CANONICAL_WORD},
        "source_curve": {
            "weighted_projective_space": "P(1,1,2)",
            "equation": "(X^3+Y^3)(2Y^3-X^3)=2W^3",
            "expanded_coefficients_X6_X3Y3_Y6_W3": list(CURVE_COEFFICIENTS),
            "genus": 4,
            "point": [str(value) for value in SOURCE_POINT],
        },
        "progression": field_and_hit_certificate(),
        "colors": {
            "raw_mod_<6>": list(raw),
            "canonical_via_c_to_2c": list(canonical),
        },
        "elliptic_quotient": nagell_lutz_nontorsion(),
        "claim_boundary": (
            "This closes existence for one model and proves its elliptic "
            "quotient has positive rank. It does not prove infinitely many "
            "rational points on the genus-four source curve."
        ),
    }


def write_certificate(path=CERTIFICATE):
    path.write_text(
        json.dumps(certificate_data(), indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    print(write_certificate())
