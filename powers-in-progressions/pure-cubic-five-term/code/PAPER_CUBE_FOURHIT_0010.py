"""Exact certificate for the endpoint-omitted four-hit branch 0010.

The counted positions are 0,1,2,3 and their colors are 0,0,1,0.  The
three rational-cube positions 0,1,3 give the same smooth plane cubic as the
previous 0001 branch.  This module freezes the distinct color/position
model, its pure-cubic lift, and the common positive-rank certificate.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "PAPER_CUBE_FOURHIT_0010_CERTIFICATE.json"
BASE_SOURCE = HERE / "PAPER_CUBE_FOURHIT_0001.py"
BASE_TEST = HERE / "PAPER_CUBE_FOURHIT_0001_test.py"
BASE_CERTIFICATE = HERE / "PAPER_CUBE_FOURHIT_0001_CERTIFICATE.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_base():
    path = BASE_SOURCE
    spec = importlib.util.spec_from_file_location("paper_cube_fourhit_0001_base", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


base = _load_base()

INDICES = (0, 1, 2, 3)
COLORS = (0, 0, 1, 0)
OLD_INDICES = (0, 1, 3, 4)
OLD_COLORS = (0, 0, 0, 1)
ORIGIN = base.ORIGIN
GENERATOR = base.GENERATOR


def curve_value(point):
    """The relation among cube positions 0,1,3."""
    return base.curve_value(point)


def progression(point):
    """Return the five rational AP entries attached to a point of C."""
    return base.progression(point)


def middle_radicand(point):
    """Return A_2, whose cube class is the singleton color in this branch."""
    return progression(point)[2]


def cube_free_representative(value: Fraction) -> tuple[int, Fraction]:
    """Write nonzero rational value as D*w^3 with positive cube-free D."""
    value = Fraction(value)
    if value == 0:
        raise ValueError("zero has no nontrivial Kummer class")

    # Factor numerator and denominator; exponents are reduced modulo 3.
    sign = -1 if value < 0 else 1
    num, den = abs(value.numerator), value.denominator

    def factor(n):
        out = {}
        p = 2
        while p*p <= n:
            while n % p == 0:
                out[p] = out.get(p, 0) + 1
                n //= p
            p += 1
        if n > 1:
            out[n] = out.get(n, 0) + 1
        return out

    exponents = factor(num)
    for p, e in factor(den).items():
        exponents[p] = exponents.get(p, 0) - e

    D = 1
    w = Fraction(sign, 1)  # -1 is itself a rational cube.
    for p, e in sorted(exponents.items()):
        residue = e % 3
        D *= p**residue
        w *= Fraction(p)**((e-residue)//3)
    assert value == D*w**3
    return D, w


def affine_color_orbit(indices, colors):
    """AGL(1,F_3) on colors together with reversal of five positions."""
    out = set()
    for slope in (1, 2):
        for shift in range(3):
            transformed = tuple((slope*c+shift) % 3 for c in colors)
            out.add((tuple(indices), transformed))
            reflected = sorted((4-i, c) for i, c in zip(indices, transformed))
            out.add((tuple(i for i, _ in reflected), tuple(c for _, c in reflected)))
    return out


def boundary_data():
    """JSON-safe algebra behind the two zero tests and fifth-hit gate.

    Coefficient vectors use the ordered basis (X^3,Y^3,Z^3).  The AP
    identities are understood on C, whose relation vector is (2,-3,1).
    """
    entries = (
        (1, 0, 0),
        (0, 1, 0),
        (-1, 2, 0),
        (0, 0, 1),
        (-3, 4, 0),
    )
    curve_relation = (2, -3, 1)
    assert tuple(entries[3][i] - 3*entries[1][i] + 2*entries[0][i]
                 for i in range(3)) == curve_relation
    assert entries[2] == (-1, 2, 0)
    assert entries[4] == (-3, 4, 0)

    extensions = tuple(COLORS + (e,) for e in range(3))
    assert all(len(word) == 5 and word[:4] == COLORS for word in extensions)
    return {
        "monomial_basis": ["X^3", "Y^3", "Z^3"],
        "entry_coefficient_vectors": [list(row) for row in entries],
        "curve_relation_vector": list(curve_relation),
        "A2_zero": {
            "coefficient_vector": list(entries[2]),
            "cleared_equation": {"X^3": 1, "Y^3": -2},
            "requires_nonzero": "Y",
            "implied_rational_ratio_cube": {"ratio": "X/Y", "value": "2"},
            "contradiction": "2 is not a rational cube",
        },
        "A4_zero": {
            "coefficient_vector": list(entries[4]),
            "cleared_equation": {"X^3": 3, "Y^3": -4},
            "requires_nonzero": "Y",
            "implied_rational_ratio_cube": {"ratio": "X/Y", "value": "4/3"},
            "contradiction": "4/3 is not a rational cube",
        },
        "fifth_hit": {
            "known_indices": list(INDICES),
            "known_color_exponents": list(COLORS),
            "remaining_index": 4,
            "kernel_allowed_remaining_exponents": [0, 1, 2],
            "extended_color_words": ["".join(map(str, word)) for word in extensions],
            "hit_count_if_condition_holds": 5,
            "proved_upper_bound": 4,
            "contradiction": True,
        },
    }


def certificate_data():
    ap = progression(GENERATOR)
    D, w = cube_free_representative(middle_radicand(GENERATOR))
    image_O = base.map_to_mordell(ORIGIN)
    image_P = base.map_to_mordell(GENERATOR)
    twice_Q = base.ec_add(base.Q, base.Q)
    three_Q = base.ec_add(twice_Q, base.Q)
    assert ap == tuple(map(Fraction, (64, 1, -62, -125, -188)))
    assert D == 62 and w == -1
    assert image_O == (base.Q[0], -base.Q[1])
    assert image_P == twice_Q
    assert base.ec_add(image_P, base.Q) == three_Q
    # Recompute the inherited cleared Mordell-map identity rather than
    # trusting only the byte hashes below.
    assert base.symbolic_map_identity() != 0
    assert affine_color_orbit(INDICES, COLORS).isdisjoint(
        affine_color_orbit(OLD_INDICES, OLD_COLORS)
    )
    return {
        "schema": "paper-cube-fourhit-0010-v2",
        "selected_orbit": {"indices": list(INDICES), "colors": "0010"},
        "distinct_from_0001_orbit": True,
        "curve_derivation": "A_3=3*A_1-2*A_0 gives 2*X^3-3*Y^3+Z^3=0",
        "curve": "2*X^3-3*Y^3+Z^3=0",
        "origin": [1, 1, 1],
        "infinite_order_point": [4, 1, -5],
        "mordell_curve": "v^2=u^3-243",
        "mordell_Q": [7, 10],
        "origin_image": [str(v) for v in image_O],
        "point_image": [str(v) for v in image_P],
        "translated_point_image": {
            "group_expression": "phi(P)-phi(O)=2Q-(-Q)=3Q",
            "coordinates": [str(v) for v in three_Q],
        },
        "nagell_lutz_discriminant": -2**4*3**13,
        "inherited_mordell_identity_dependency": {
            "source": {"filename": BASE_SOURCE.name, "sha256": sha256(BASE_SOURCE)},
            "test": {"filename": BASE_TEST.name, "sha256": sha256(BASE_TEST)},
            "base_certificate": {
                "filename": BASE_CERTIFICATE.name,
                "sha256": sha256(BASE_CERTIFICATE),
            },
            "recomputed_function": "symbolic_map_identity",
            "cleared_identity_recomputed": True,
        },
        "sample": {
            "AP": [str(v) for v in ap],
            "counted_positions": list(INDICES),
            "counted_roots": ["4", "1", "-cuberoot(62)", "-5"],
            "D": D,
            "middle_scale": str(w),
        },
        "boundary": {
            "structured_algebra": boundary_data(),
            "zero_coordinate_ratios": ["3", "-2", "3/2"],
            "A2_zero_would_make_cube": "2",
            "A4_zero_would_make_cube": "4/3",
            "constant_point": [1, 1, 1],
            "A2_non_cube_reason": "otherwise positions 0,1,2,3 are four rational cubes, contradicting P_5(3)=3",
            "fifth_hit_excluded_by": "R^times_(3,1)(5)=4",
        },
        "classification_boundary": (
            "This proves an infinite family in the single additional orbit "
            "((0,1,2,3),0010); the other 29 unresolved models are not classified"
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
