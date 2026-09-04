"""Exact classification of five rank-zero quotient clusters in Round 11."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "PAPER_CUBE_FOURHIT_RANKZERO_ROUND11_CERTIFICATE.json"

# Each representative is a genus-four cover
# a*X^6+b*X^3*Y^3+c*Y^6+w*W^3=0 with quotient v^2=u^3+1.
# The first two nontrivial cluster keys below each have a second Round-09
# model obtained by swapping X and Y.
REPRESENTATIVES = (
    {
        "name": "endpoint-omitted-0120",
        "indices": (0, 1, 2, 3), "word": "0120",
        "repeated": (0, 3), "singletons": (1, 2),
        "coefficients": (2, 5, 2, -9),
        "cluster_key": ("2+1+1", 2, 5, 2, -9),
        "cluster_members": (((0, 1, 2, 3), "0120"),),
    },
    {
        "name": "endpoint-omitted-0102",
        "indices": (0, 1, 2, 3), "word": "0102",
        "repeated": (0, 2), "singletons": (1, 3),
        "coefficients": (-1, 2, 3, -4),
        "cluster_key": ("2+1+1", 1, -2, -3, 4),
        "cluster_members": (
            ((0, 1, 2, 3), "0121"),
            ((0, 1, 2, 3), "0102"),
        ),
    },
    {
        "name": "endpoint-omitted-0012",
        "indices": (0, 1, 2, 3), "word": "0012",
        "repeated": (0, 1), "singletons": (2, 3),
        "coefficients": (2, -7, 6, -1),
        "cluster_key": ("2+1+1", 2, -7, 6, -1),
        "cluster_members": (
            ((0, 1, 2, 3), "0122"),
            ((0, 1, 2, 3), "0012"),
        ),
    },
    {
        "name": "position3-omitted-0121",
        "indices": (0, 1, 2, 4), "word": "0121",
        "repeated": (1, 4), "singletons": (0, 2),
        "coefficients": (8, 2, -1, -9),
        "cluster_key": ("2+1+1", 1, -2, -8, 9),
        "cluster_members": (((0, 1, 2, 4), "0121"),),
    },
    {
        "name": "position3-omitted-0112",
        "indices": (0, 1, 2, 4), "word": "0112",
        "repeated": (1, 2), "singletons": (0, 4),
        "coefficients": (-4, 8, -3, -1),
        "cluster_key": ("2+1+1", 3, -8, 4, 1),
        "cluster_members": (((0, 1, 2, 4), "0112"),),
    },
)

E_POINTS = (None, (-1, 0), (0, -1), (0, 1), (2, -3), (2, 3))


def integer_cube_root(value: int) -> int | None:
    sign = -1 if value < 0 else 1
    root, exact = sp.integer_nthroot(abs(value), 3)
    return sign*int(root) if exact else None


def rational_cube_root(value: Fraction) -> Fraction | None:
    value = Fraction(value)
    numerator = integer_cube_root(value.numerator)
    denominator = integer_cube_root(value.denominator)
    if numerator is None or denominator is None:
        return None
    return Fraction(numerator, denominator)


def is_rational_cube(value: Fraction) -> bool:
    return rational_cube_root(Fraction(value)) is not None


def curve_value(coefficients, point) -> Fraction:
    a, b, c, w = coefficients
    x, y, z = map(Fraction, point)
    return a*x**6+b*x**3*y**3+c*y**6+w*z**3


def quotient_constants(coefficients):
    """Return A, discriminant and scale with A^2*disc=scale^6."""
    a, b, c, w = coefficients
    A = -4*a*w
    discriminant = b*b-4*a*c
    K = A*A*discriminant
    scale, exact = sp.integer_nthroot(K, 6)
    assert exact
    return A, discriminant, int(scale)


def quotient_map(representative, point):
    """Map the affine Y!=0 part to E: v^2=u^3+1."""
    x, y, z = map(Fraction, point)
    if y == 0:
        raise ZeroDivisionError("quotient formula uses Y != 0")
    a, b, _, _ = representative["coefficients"]
    A, _, scale = quotient_constants(representative["coefficients"])
    t3 = (x/y)**3
    z_affine = z/y**2
    u = Fraction(A, scale**2)*z_affine
    v = Fraction(A, scale**3)*(2*a*t3+b)
    assert v*v == u**3+1
    return u, v


def primitive_cover_rhs(a: int, b: int, d: int, U: int, V: int) -> int:
    assert b % d == 0
    return d*U**4+a*U**2*V**2+(b//d)*V**4


def primitive_square_residues(a: int, b: int, d: int, modulus: int):
    squares = {n*n % modulus for n in range(modulus)}
    out = []
    for U in range(modulus):
        for V in range(modulus):
            if math.gcd(math.gcd(U, V), modulus) != 1:
                continue
            rhs = primitive_cover_rhs(a, b, d, U, V) % modulus
            if rhs in squares:
                out.append((U, V, rhs))
    return tuple(out)


def descent_data():
    """Exact 2-isogeny descent certificate for v^2=u^3+1."""
    # Shift x=u+1: v^2=x^3-3x^2+3x, with 2-torsion (0,0).
    E = {"a": -3, "b": 3}
    # For d=-1,-3 the cover quartics are negative definite.
    E_negative = {-1: (-1, -3, -3), -3: (-3, -3, -1)}
    # The isogenous curve is y^2=x^3+6x^2-3x.  Its d=-1,3
    # primitive covers have no solution modulo 16.
    Eprime = {"a": 6, "b": -3}
    obstructions = {
        d: primitive_square_residues(Eprime["a"], Eprime["b"], d, 16)
        for d in (-1, 3)
    }
    assert all(not residues for residues in obstructions.values())
    image_E = (1, 3)       # realized by O and (0,0)
    image_Eprime = (1, -3) # realized by O and (0,0)
    two_to_rank = len(image_E)*len(image_Eprime)//4
    assert two_to_rank == 1
    return {
        "shifted_E": E,
        "E_negative_definite_cover_coefficients": {
            str(d): list(coeffs) for d, coeffs in E_negative.items()
        },
        "E_image_squareclasses": list(image_E),
        "two_isogenous_Eprime": Eprime,
        "Eprime_modulus": 16,
        "Eprime_obstructed_squareclasses": [-1, 3],
        "Eprime_primitive_solution_residue_counts": {
            str(d): len(residues) for d, residues in obstructions.items()
        },
        "Eprime_image_squareclasses": list(image_Eprime),
        "two_to_rank": two_to_rank,
        "rank": 0,
    }


def nagell_lutz_points():
    """Enumerate all torsion after rank zero, using discriminant -432."""
    discriminant = -432
    points = [None]
    for y_abs in range(math.isqrt(abs(discriminant))+1):
        if y_abs and discriminant % (y_abs*y_abs) != 0:
            continue
        x = integer_cube_root(y_abs*y_abs-1)
        if x is None:
            continue
        if y_abs == 0:
            points.append((x, 0))
        else:
            points.extend(((x, -y_abs), (x, y_abs)))
    assert tuple(points) == E_POINTS
    return E_POINTS


def rational_preimages(representative):
    """Enumerate all rational affine preimages of E(Q)."""
    a, b, _, w = representative["coefficients"]
    A, _, scale = quotient_constants(representative["coefficients"])
    out = []
    for point in nagell_lutz_points():
        if point is None:
            continue
        u, v = point
        z = Fraction(u*scale**2, A)
        t3 = (Fraction(v*scale**3, A)-b)/(2*a)
        t = rational_cube_root(t3)
        if t is not None:
            lifted = (t, Fraction(1), z)
            assert curve_value(representative["coefficients"], lifted) == 0
            out.append((point, lifted))
    # At Y=0 a rational point would force (W/X^2)^3=-a/w.
    assert rational_cube_root(Fraction(-a, w)) is None
    return tuple(out)


def progression(representative, point):
    """Recover the rational AP from the repeated-color cube positions."""
    X, Y, _ = map(Fraction, point)
    p, q = representative["repeated"]
    values = tuple(
        Fraction((q-k)*X**3+(k-p)*Y**3, q-p)
        for k in range(5)
    )
    assert len({values[k+1]-values[k] for k in range(4)}) == 1
    return values


def pure_cubic_class(value: Fraction, radicand: int):
    for exponent in range(3):
        if is_rational_cube(Fraction(value, radicand**exponent)):
            return exponent
    return None


def representative_results():
    out = []
    for representative in REPRESENTATIVES:
        rows = []
        for elliptic_point, lifted in rational_preimages(representative):
            rows.append({
                "elliptic_point": list(elliptic_point),
                "affine_X_Y_W": [str(value) for value in lifted],
                "AP": [str(value) for value in progression(representative, lifted)],
            })
        out.append({
            "name": representative["name"],
            "cluster_key": list(representative["cluster_key"]),
            "cluster_members": [
                {"indices": list(indices), "word": word}
                for indices, word in representative["cluster_members"]
            ],
            "coefficients_X6_X3Y3_Y6_W3": list(representative["coefficients"]),
            "quotient": "v^2=u^3+1",
            "all_rational_affine_preimages": rows,
            "rational_point_at_infinity": False,
        })
    return out


def certificate_data():
    results = representative_results()
    selected = next(
        r for r in REPRESENTATIVES if r["name"] == "position3-omitted-0121"
    )
    exceptional = (Fraction(-1, 2), Fraction(1), Fraction(-1, 2))
    ap = progression(selected, exceptional)
    integer_ap = tuple(value*8 for value in ap)
    assert integer_ap == (-4, -1, 2, 5, 8)
    classes = tuple(pure_cubic_class(value, 4) for value in integer_ap)
    assert classes == (1, 0, 2, None, 0)
    return {
        "schema": "paper-cube-fourhit-rankzero-round11-v1",
        "theorem": {
            "rank_zero_clusters_classified": 5,
            "explicit_models_classified": 7,
            "models_with_no_admissible_nonconstant_nonzero_point": 6,
            "models_with_one_admissible_projective_class": 1,
            "remaining_unclassified_models": 18,
        },
        "elliptic_quotient": {
            "curve": "v^2=u^3+1", "discriminant": -432,
            "descent": descent_data(),
            "rational_points": [None if p is None else list(p) for p in E_POINTS],
        },
        "representatives": results,
        "unique_nonconstant_example": {
            "model": {"indices": [0, 1, 2, 4], "word": "0121"},
            "weighted_projective_point": [-1, 2, -2],
            "integer_AP": list(integer_ap),
            "field": "Q(cuberoot(2))=Q(cuberoot(4))",
            "raw_classes_for_D=4": [
                value if value is not None else "not in <D>" for value in classes
            ],
            "raw_word_on_indices_0_1_2_4": "1020",
            "canonical_color_map": "c -> 2c+1 gives 0121",
        },
        "boundary_point": {
            "representative": "endpoint-omitted-0102",
            "affine_X_Y_W": [-1, 1, 0], "AP": [-1, 0, 1, 2, 3],
            "reason_inadmissible": "zero occurs at counted position 1",
        },
        "claim_boundary": (
            "The rank-zero quotient classifies five permutation clusters, "
            "covering seven explicit models. It gives no infinite family; "
            "the six earlier genus-one models remain the only proved infinite "
            "families, and 18 genus-four models remain unclassified."
        ),
    }


def write_certificate(path: Path = CERTIFICATE):
    path.write_text(
        json.dumps(certificate_data(), indent=2)+"\n",
        encoding="utf-8", newline="\n",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    print(write_certificate())
