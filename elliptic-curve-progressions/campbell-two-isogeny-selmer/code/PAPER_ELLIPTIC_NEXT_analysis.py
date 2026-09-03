"""Exact next-stage checks for the Moody--Juyal and Campbell branches.

This module proves polynomial identities and builds a first-stage *local witness*
matrix for the 32+32 isogeny-cover candidates.  A missing witness is explicitly
inconclusive; it is never reported as a local obstruction.
"""

from __future__ import annotations

from itertools import combinations
from math import prod

import sympy as sp


c, m, r = sp.symbols("c m r")


def mj_t(cc=c, mm=m):
    return sp.factor((cc * mm**2 - 4 * (cc - 1) ** 2) / (2 * cc * mm))


def mj_y(cc=c, mm=m):
    return sp.factor(-(cc * mm**2 + 4 * (cc - 1) ** 2) / (4 * mm))


# If x=c is parameterized as in Moody--Juyal section 3.2 and x=rc is
# forced to be another point, then (4m*y_rc)^2=Q_R.
G_R = (
    16 * c**4 * r
    + 16 * c**3 * m**2 * r**2
    - 8 * c**3 * m**2 * r
    - 64 * c**3 * r
    + c**2 * m**4 * r
    - 16 * c**2 * m**2 * r
    + 96 * c**2 * r
    - 8 * c * m**2 * r
    + 16 * c * m**2
    - 64 * c * r
    + 16 * r
)
Q_R = sp.expand(r * G_R)


# Triple-contact parabola at the boundary point (c,z)=(0,4r).  At r=3,
# its fourth intersection is exactly the formula printed in MJ section 3.2.
B_TAN = -m**2 * r + 2 * m**2 - 8 * r
A_TAN = -(
    -m**4 * r + m**4 + 8 * m**2 * r**2 - 8 * m**2 * r - 8 * r**2
) / (2 * r)
Z_TAN = sp.factor(4 * r + B_TAN * c + A_TAN * c**2)
C_TAN = sp.factor(
    4
    * r
    * (
        m**4 * r
        - 2 * m**4
        - 8 * m**2 * r**2
        + 24 * m**2 * r
        + 16 * r**3
        - 48 * r**2
    )
    / (
        (-m**2 + 8 * r)
        * (-m**4 * r + m**4 + 8 * m**2 * r**2 - 8 * m**2 * r - 16 * r**2)
    )
)


# A different boundary chord through c=0 and c=1/r (where rc=1 is the
# fixed order-4 x-coordinate).  Its third intersection specializes at r=2
# to the endpoint section found in the feasibility package.
B_CHORD = r * m**2 - 8 * r**2 + 8 * r - 8
Z_CHORD = 4 * r * c**2 + B_CHORD * c + 4 * r
C_CHORD = sp.factor(r * (4 * r - 4 - m**2) / (r * m**2 + 4 * r - 4))


def general_r_identities():
    tt = mj_t()
    aa = tt**2 / 4 - 2
    rhs_rc = sp.factor(r * c * ((r * c) ** 2 + aa * r * c + 1))
    tangent_remainder = sp.factor((Q_R - Z_TAN**2) / c**3)
    chord_remainder = sp.factor(Q_R - Z_CHORD**2)
    published_r3 = 6 * m**4 / ((m**2 - 24) * (m**4 - 24 * m**2 + 72))
    endpoint_r2 = (4 - m**2) / (m**2 + 2)
    return {
        "quartic_elimination": sp.factor(rhs_rc - Q_R / (16 * m**2)),
        "tangent_vanish_c0_order3": [
            sp.Poly(Q_R - Z_TAN**2, c).coeff_monomial(c**i) for i in range(3)
        ],
        "tangent_factor_after_c3": tangent_remainder,
        "tangent_section_on_quartic": sp.factor(
            (Q_R - Z_TAN**2).subs(c, C_TAN)
        ),
        "published_r3_match": sp.factor(C_TAN.subs(r, 3) - published_r3),
        "tangent_r2": sp.factor(C_TAN.subs(r, 2)),
        "chord_factorization": chord_remainder,
        "chord_section_on_quartic": sp.factor(
            (Q_R - Z_CHORD**2).subs(c, C_CHORD)
        ),
        "endpoint_r2_match": sp.factor(C_CHORD.subs(r, 2) - endpoint_r2),
        "two_r2_sections_difference": sp.factor(
            C_TAN.subs(r, 2) - C_CHORD.subs(r, 2)
        ),
    }


# Centered y-AP slice.  For P=(x,s), Q=(z,-s), put p=x+z and h=xz.
# On p=1-h, h=rho^2, rational x,z require eta^2=rho^4-6rho^2+1.
rho, eta = sp.symbols("rho eta")
Y_SLICE_QUARTIC = rho**4 - 6 * rho**2 + 1


def y_slice_to_jacobian(rr=rho, ee=eta):
    big_u = sp.cancel((ee + 1) / rr**2)
    XX = sp.factor(2 * big_u - 6)
    YY = sp.factor(2 * rr * (big_u**2 - 1))
    return XX, YY


def y_slice_from_jacobian(XX, YY):
    """Inverse on the common affine open rho*Y*(X+4)*(X+8) != 0."""
    denominator = (XX + 4) * (XX + 8)
    rr = sp.factor(2 * YY / denominator)
    ee = sp.factor((XX**2 - 32) / denominator)
    return rr, ee


def y_slice_boundary_map():
    """The four omitted quartic points and their images on the Jacobian.

    The two strings ``infinity_+/-`` denote the points with eta/rho^2 -> +/-1.
    """
    return {
        "rho=0,eta=+1": "O",
        "rho=0,eta=-1": (0, 0),
        "infinity_+": (-4, 0),
        "infinity_-": (-8, 0),
    }


def y_slice_identities():
    p, h, x, z, s, tt = sp.symbols("p h x z s tt")
    aa = -(p**2 - h + 1) / p
    square = h * (1 - h) / p
    t_square = 4 * (-p**2 + 2 * p + h - 1) / p
    XJ, YJ = y_slice_to_jacobian()
    rho_back, eta_back = y_slice_from_jacobian(XJ, YJ)
    jac_num = sp.together(YJ**2 - XJ * (XJ + 4) * (XJ + 8)).as_numer_denom()[0]
    return {
        "equal_height_first": sp.factor(
            (x * (x**2 + aa * x + 1) - square).subs(
                {p: x + z, h: x * z}
            )
        ),
        "t_formula": sp.factor(4 * (aa + 2) - t_square),
        "slice_s_square": sp.factor(
            square.subs(p, 1 - h).subs(h, rho**2) - rho**2
        ),
        "slice_t_square": sp.factor(
            t_square.subs(p, 1 - h).subs(h, rho**2) - 4 * rho**2
        ),
        "root_discriminant": sp.factor(
            (1 - rho**2) ** 2 - 4 * rho**2 - Y_SLICE_QUARTIC
        ),
        "jacobian_map": sp.factor(
            sp.rem(jac_num, eta**2 - Y_SLICE_QUARTIC, eta)
        ),
        "inverse_rho": sp.factor(
            sp.rem(sp.together(rho_back - rho).as_numer_denom()[0],
                   eta**2 - Y_SLICE_QUARTIC, eta)
        ),
        "inverse_eta": sp.factor(
            sp.rem(sp.together(eta_back - eta).as_numer_denom()[0],
                   eta**2 - Y_SLICE_QUARTIC, eta)
        ),
        # If p=1-rho^2 vanished then the quartic would give eta^2=-4.
        "p_zero_forces_eta_square_plus_4": sp.factor(
            Y_SLICE_QUARTIC.subs(rho**2, 1) + 4
        ),
        # On rho != 0, Y=0 would force U=+/-1.  Substitution in the
        # quartic gives respectively 4*rho^2=0 or 8*rho^2=0.
        "Y_zero_U_plus_obstruction": sp.factor(
            (rho**2 - 1) ** 2 - Y_SLICE_QUARTIC - 4 * rho**2
        ),
        "Y_zero_U_minus_obstruction": sp.factor(
            (-rho**2 - 1) ** 2 - Y_SLICE_QUARTIC - 8 * rho**2
        ),
    }


def squareclasses(primes):
    values = []
    for sign in (1, -1):
        for size in range(len(primes) + 1):
            for subset in combinations(primes, size):
                values.append(sign * prod(subset))
    return sorted(values)


BAD_PRIMES = [2, 3, 5, 7, 59, 71699, 339106321]
MODULUS_DEPTHS = {2: 8, 3: 6, 5: 5, 7: 4}
SIDES = {
    "E": {
        "a": -591895071,
        "b": 58536289153843200,
        "support": [2, 3, 5, 7],
    },
    "E_dual": {
        "a": 1183790142,
        "b": 116194618458722241,
        "support": [3, 59, 71699, 339106321],
    },
}


def real_status(d, a, b):
    if d > 0:
        return "REAL_YES_INFINITY"
    if a <= 0:
        return "REAL_NO_SIGN"
    # For the dual side a^2-4b=16*b_E >0, so the quadratic in s=(U/V)^2
    # has a positive maximum between two positive roots.
    if a * a - 4 * b > 0:
        return "REAL_YES_INTERVAL"
    return "REAL_UNRESOLVED"


def vp(n, p):
    if n == 0:
        return 10**9
    n = abs(n)
    result = 0
    while n % p == 0:
        n //= p
        result += 1
    return result


def odd_p_square(n, p):
    if n == 0:
        return True
    valuation = vp(n, p)
    unit = (n // (p**valuation)) % p
    return valuation % 2 == 0 and pow(unit, (p - 1) // 2, p) == 1


def odd_p_witness(d, a, b, p, search_bound=256):
    """Find an exact Q_p point by a square RHS, or return None.

    Since every d is a signed squarefree divisor of b, b//d is integral.
    The valuation/unit criterion is necessary and sufficient for a nonzero
    rational integer to be a square in Q_p.  Failure of this bounded witness
    search is deliberately inconclusive.
    """
    assert p % 2 == 1 and b % d == 0
    bd = b // d
    for uv_chart, values in (
        ("V=1", range(min(p, search_bound))),
        ("U=1", range(min(p, search_bound))),
    ):
        for value in values:
            if uv_chart == "V=1":
                U, V = value, 1
            else:
                U, V = 1, value
            rhs = d * U**4 + a * U**2 * V**2 + bd * V**4
            if rhs != 0 and odd_p_square(rhs, p):
                valuation = vp(rhs, p)
                return {
                    "chart": uv_chart,
                    "value": value,
                    "valuation": valuation,
                    "unit_mod_p": (rhs // p**valuation) % p,
                }
    return None


def v2(n):
    if n == 0:
        return 10**9
    n = abs(n)
    result = 0
    while n % 2 == 0:
        n //= 2
        result += 1
    return result


def q2_square(n):
    if n == 0:
        return True
    valuation = v2(n)
    return valuation % 2 == 0 and ((n >> valuation) % 8 == 1)


def q2_witness(d, a, b, search_bound=128):
    assert b % d == 0
    bd = b // d
    for chart, values in (("V=1", range(search_bound)), ("U=1", range(search_bound))):
        for value in values:
            U, V = (value, 1) if chart == "V=1" else (1, value)
            rhs = d * U**4 + a * U**2 * V**2 + bd * V**4
            if rhs != 0 and q2_square(rhs):
                return {"chart": chart, "value": value, "rhs": rhs}
    return None


def has_projective_solution_mod_prime_power(d, a, b, p, exponent):
    """Exhaust P^1(Z/p^exponent) and test whether the RHS is a square.

    Representatives are (U:1) and (1:V) with p|V.  Hence a negative result
    is a rigorous Q_p obstruction: weighted projective scaling can make U,V
    integral with at least one a unit and N integral.  Thus the reduction is
    represented by a primitive integer pair (U,V); it need not make the affine
    ratio U/V an integer.
    """
    assert b % d == 0
    modulus = p**exponent
    squares = {value * value % modulus for value in range(modulus)}
    bd = b // d
    for U in range(modulus):
        if (d * U**4 + a * U**2 + bd) % modulus in squares:
            return True
    for V in range(0, modulus, p):
        if (d + a * V**2 + bd * V**4) % modulus in squares:
            return True
    return False


def campbell_local_matrix():
    rows = []
    for side, data in SIDES.items():
        a, b = data["a"], data["b"]
        for d in squareclasses(data["support"]):
            row = {
                "side": side,
                "d": d,
                "infinity": real_status(d, a, b),
                "places": {},
            }
            for p in BAD_PRIMES:
                if p == 2:
                    witness = q2_witness(d, a, b)
                    if witness:
                        cell = {"status": "Q2_YES_EXACT_SQUARE", "witness": witness}
                    elif not has_projective_solution_mod_prime_power(
                        d, a, b, p, MODULUS_DEPTHS[p]
                    ):
                        cell = {
                            "status": "QP_NO_MODULUS",
                            "modulus": p ** MODULUS_DEPTHS[p],
                        }
                    else:
                        cell = {"status": "Q2_UNRESOLVED"}
                    row["places"][str(p)] = cell
                else:
                    witness = odd_p_witness(d, a, b, p)
                    if witness:
                        cell = {
                            "status": "QP_YES_EXACT_SQUARECLASS",
                            "witness": witness,
                        }
                    elif p in MODULUS_DEPTHS and not has_projective_solution_mod_prime_power(
                        d, a, b, p, MODULUS_DEPTHS[p]
                    ):
                        cell = {
                            "status": "QP_NO_MODULUS",
                            "modulus": p ** MODULUS_DEPTHS[p],
                        }
                    else:
                        cell = {
                            "status": "QP_UNRESOLVED_NO_SMALL_UNIT_WITNESS"
                        }
                    row["places"][str(p)] = cell
            rows.append(row)
    return rows


def matrix_summary(rows=None):
    rows = campbell_local_matrix() if rows is None else rows
    real_no = [row for row in rows if row["infinity"] == "REAL_NO_SIGN"]
    resolved = 0
    unresolved = 0
    finite_obstructed = 0
    for row in rows:
        for cell in row["places"].values():
            if "YES" in cell["status"]:
                resolved += 1
            elif cell["status"] == "QP_NO_MODULUS":
                finite_obstructed += 1
            else:
                unresolved += 1
    survivors = [
        row
        for row in rows
        if row["infinity"] != "REAL_NO_SIGN"
        and all(cell["status"] != "QP_NO_MODULUS" for cell in row["places"].values())
    ]
    return {
        "rows": len(rows),
        "real_obstructed": len(real_no),
        "finite_obstruction_cells": finite_obstructed,
        "finite_cells_proved_nonempty": resolved,
        "finite_cells_unresolved": unresolved,
        "survivors_after_proven_obstructions": {
            side: [row["d"] for row in survivors if row["side"] == side]
            for side in SIDES
        },
        "warning": "Unresolved is not locally insoluble and is not a Selmer result.",
    }


def validate():
    gi = general_r_identities()
    assert gi["quartic_elimination"] == 0
    assert gi["tangent_vanish_c0_order3"] == [0, 0, 0]
    assert gi["tangent_section_on_quartic"] == 0
    assert gi["published_r3_match"] == 0
    assert gi["chord_section_on_quartic"] == 0
    assert gi["endpoint_r2_match"] == 0
    assert gi["two_r2_sections_difference"] != 0
    yi = y_slice_identities()
    assert all(value == 0 for value in yi.values())
    rows = campbell_local_matrix()
    assert len(rows) == 64
    assert len({(row["side"], row["d"]) for row in rows}) == 64
    summary = matrix_summary(rows)
    assert summary["real_obstructed"] == 16
    return gi, yi, rows, summary


if __name__ == "__main__":
    import json

    _, _, rows, summary = validate()
    print(json.dumps({"summary": summary, "rows": rows}, indent=2, sort_keys=True))
