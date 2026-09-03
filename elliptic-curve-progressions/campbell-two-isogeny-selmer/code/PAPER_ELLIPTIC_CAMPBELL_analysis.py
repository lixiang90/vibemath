"""Exact second-stage local matrix and torsor audit for Campbell's ninth point.

The 64-row matrix starts from PAPER_ELLIPTIC_NEXT_analysis and replaces every
formerly unresolved cell by a valuation-normalized proof.  It also reconstructs
H(m)=g_m(8) and computes the rational component of the binary-quartic Cassels
class.  No Selmer group or rational-point completeness claim is made.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import PAPER_ELLIPTIC_NEXT_analysis as nxt


ROOT = Path(__file__).resolve().parent
CERT_ROOT = ROOT.parent / "certificates"
SCRIPT_PATH = ROOT / "PAPER_ELLIPTIC_CAMPBELL_analysis.py"
NEXT_PATH = ROOT / "PAPER_ELLIPTIC_NEXT_analysis.py"
CERTIFICATE_PATH = CERT_ROOT / "local_matrix_512.json"

M = sp.symbols("m")
H_COEFFS = (-850079, -11210976, 138714149248, -5501355374592, -1679721044504576)
H = sp.Poly.from_list(H_COEFFS, gens=M).as_expr()

# Campbell Theorem 2.5, evaluated at x=8.
G3 = -18816*M**4 + 677376*M**3 + 1922543616*M**2 - 48944480256*M - 40678301368320
G2 = 236896*M**4 - 9821952*M**3 - 22598349824*M**2 + 508953231360*M + 520252184657920
G1 = -958800*M**4 + 40985280*M**3 + 89932669440*M**2 - 1957723729920*M - 2113363439616000
G0 = 1292769*M**4 - 57304800*M**3 - 118795148928*M**2 + 2647001548800*M + 2758336954896384


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def factor_dict(value: int) -> dict[str, int]:
    sign = -1 if value < 0 else 1
    result = {str(p): int(e) for p, e in sp.factorint(abs(value)).items()}
    if sign < 0:
        result["-1"] = 1
    return result


def squarefree_part(value: int) -> int:
    result = -1 if value < 0 else 1
    for prime, exponent in sp.factorint(abs(value)).items():
        if exponent % 2:
            result *= int(prime)
    return result


def binary_quartic_invariants(coefficients=H_COEFFS) -> tuple[int, int]:
    a, b, c, d, e = coefficients
    I = 12*a*e - 3*b*d + c*c
    J = 72*a*c*e + 9*b*c*d - 27*a*d*d - 27*b*b*e - 2*c**3
    return I, J


def torsor_projection_certificate() -> dict[str, object]:
    """Rational factor of the Cassels class z(H) in the split cubic algebra.

    We use Cremona's conventions: f(phi)=phi^3-3I phi+J and
    z(H)=(4*a*phi+g4(1,0))/3, with g4(1,0)=3*b^2-8*a*c.
    The rational component is the squareclass attached to the rational
    2-torsion point.  The 64-scaling and translation identify it with the
    E-side homogeneous-space parameter d=[X_new].
    """
    a, b, c, _, _ = H_COEFFS
    I, J = binary_quartic_invariants()
    phi = 269378023424
    X = sp.symbols("X")
    resolvent = sp.Poly(X**3 - 3*I*X + J, X)
    quotient, remainder = sp.div(resolvent, sp.Poly(X - phi, X))
    assert remainder.is_zero
    g4_at_10 = 3*b*b - 8*a*c
    z_q = (4*a*phi + g4_at_10) // 3
    assert 3*z_q == 4*a*phi + g4_at_10
    z_norm = int(sp.resultant(resolvent.as_expr(), g4_at_10 + 4*a*X, X) // 27)
    z_norm_root = int(sp.sqrt(z_norm))
    assert z_norm_root*z_norm_root == z_norm

    scale_u = 64
    big_root = -3*phi
    small_root = big_root // scale_u**2
    assert big_root == scale_u**2 * small_root
    assert small_root == -197298357
    # X_new=x_small-small_root=x_small+197298357.  Hence
    # x_big+3phi=64^2*X_new, a square multiple.
    return {
        "binary_quartic_H_coefficients": list(H_COEFFS),
        "H_equals_Campbell_g_at_x_8": sp.expand(G3*8**3 + G2*8**2 + G1*8 + G0 - H) == 0,
        "I": I,
        "J": J,
        "resolvent_coefficients": [int(v) for v in resolvent.all_coeffs()],
        "rational_resolvent_root_phi": phi,
        "quadratic_resolvent_factor_coefficients": [int(v) for v in quotient.all_coeffs()],
        "g4_at_1_0": g4_at_10,
        "full_cubic_algebra_class": {
            "algebra": "Q[phi]/(phi^3-3*I*phi+J) = Q x Q(sqrt(1434501462453361))",
            "representative": "(943720940177342464-3400316*phi)/3",
            "norm": z_norm,
            "norm_square_root": z_norm_root,
        },
        "z_rational_component": z_q,
        "z_rational_component_factorization": factor_dict(z_q),
        "z_rational_component_squareclass": squarefree_part(z_q),
        "large_to_small_weierstrass_scaling_u": scale_u,
        "large_rational_2_torsion_x": big_root,
        "small_rational_2_torsion_x": small_root,
        "translated_model": {
            "equation": "y^2=X^3-591895071*X^2+58536289153843200*X",
            "coordinate": "X=x_small+197298357",
        },
        "projection_to_isogeny_ambient_class": {
            "side": "E",
            "d": squarefree_part(z_q),
            "identity": "x_big+3*phi=64^2*(x_small+197298357)=64^2*X",
            "meaning": (
                "This is the rational-2-torsion component of the H^1(Q,J_H[2]) "
                "class of C_H, not a claim that C_H is isomorphic to the displayed C_d quartic."
            ),
        },
    }


def pair_from_witness(witness: dict[str, object]) -> tuple[int, int]:
    value = int(witness["value"])
    return (value, 1) if witness["chart"] == "V=1" else (1, value)


def quartic_rhs(side: str, d: int, U: int, V: int) -> int:
    data = nxt.SIDES[side]
    a, b = data["a"], data["b"]
    assert b % d == 0
    return d*U**4 + a*U**2*V**2 + (b//d)*V**4


def legendre(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        return 0
    answer = pow(value, (prime - 1)//2, prime)
    return -1 if answer == prime - 1 else int(answer)


def resolve_three_adic(d: int) -> dict[str, object]:
    """Exact witness for every formerly unresolved E-side Q_3 cell."""
    U = 3 if d % 3 == 0 else 9
    V = 1
    rhs = quartic_rhs("E", d, U, V)
    valuation = nxt.vp(rhs, 3)
    unit = (rhs // 3**valuation) % 3
    assert valuation == (4 if d % 3 == 0 else 6)
    assert valuation % 2 == 0 and unit == 1
    return {
        "status": "YES",
        "method": "valuation_normalized_integer_pair",
        "depth": "exact_Q3_squareclass",
        "witness": {"U": U, "V": V, "rhs": rhs, "valuation": valuation, "unit_mod_3": unit},
        "proof": (
            "If v3(d)=1 use (U,V)=(3,1), giving v3(rhs)=4 and unit 1 mod 3; "
            "otherwise use (9,1), giving valuation 6 and unit 1 mod 3."
        ),
    }


def multiplicative_prime_obstruction(d: int, prime: int) -> dict[str, object]:
    """Exact local obstruction when v_p(a^2-4b)=1 and d is a nonsquare unit."""
    assert prime in (59, 71699)
    a, b = nxt.SIDES["E"]["a"], nxt.SIDES["E"]["b"]
    delta = a*a - 4*b
    assert nxt.vp(delta, prime) == 1
    assert nxt.vp(2*d*b, prime) == 0
    assert legendre(d, prime) == -1
    return {
        "status": "NO",
        "method": "valuation_normalized_double_root_obstruction",
        "depth": {"v_p_delta_exact": 1, "unit_level": 1},
        "data": {
            "prime": prime,
            "delta": delta,
            "v_p_delta": 1,
            "legendre_d": -1,
            "v_p_2db": 0,
            "identity": "4*d*F_d=(2*d*U^2+a*V^2)^2-delta*V^4",
        },
        "proof": (
            "For a primitive (U,V), if p|V then F_d is d times a fourth power mod p, "
            "a nonsquare.  If V is a unit and A=2dU^2+aV^2 is a unit, the same "
            "identity makes F_d a nonsquare mod p.  If p|A, the numerator has exact "
            "valuation 1 because v_p(delta)=1, so F_d has odd valuation."
        ),
    }


def normalize_existing_cell(side: str, d: int, prime: int, cell: dict[str, object]) -> dict[str, object]:
    status = str(cell["status"])
    if "YES" in status:
        witness = dict(cell["witness"])
        U, V = pair_from_witness(witness)
        rhs = quartic_rhs(side, d, U, V)
        return {
            "status": "YES",
            "method": "exact_integer_pair_Qp_squareclass",
            "depth": "exact_Qp_squareclass",
            "witness": {**witness, "U": U, "V": V, "rhs": rhs},
            "previous_status": status,
        }
    if status == "QP_NO_MODULUS":
        exponent = nxt.MODULUS_DEPTHS[prime]
        return {
            "status": "NO",
            "method": "exhaustive_weighted_projective_mod_prime_power",
            "depth": {"prime": prime, "exponent": exponent, "modulus": prime**exponent},
            "previous_status": status,
        }
    if "UNRESOLVED" in status:
        if side != "E":
            raise AssertionError((side, d, prime, status))
        if prime == 3:
            result = resolve_three_adic(d)
        elif prime in (59, 71699):
            result = multiplicative_prime_obstruction(d, prime)
        else:
            raise AssertionError((side, d, prime, status))
        result["previous_status"] = status
        return result
    raise AssertionError(status)


def complete_local_matrix() -> list[dict[str, object]]:
    rows = []
    for old in nxt.campbell_local_matrix():
        side, d = old["side"], old["d"]
        real_yes = old["infinity"] != "REAL_NO_SIGN"
        places: dict[str, dict[str, object]] = {
            "infinity": {
                "status": "YES" if real_yes else "NO",
                "method": old["infinity"],
                "depth": "exact_real_sign_analysis",
            }
        }
        for prime_text, cell in old["places"].items():
            prime = int(prime_text)
            places[prime_text] = normalize_existing_cell(side, d, prime, cell)
        rows.append({"side": side, "d": d, "places": places})
    assert len(rows) == 64
    return rows


def matrix_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    counts = {"YES": 0, "NO": 0, "UNRESOLVED": 0}
    old_unresolved_resolutions = {"YES": 0, "NO": 0, "UNRESOLVED": 0}
    for row in rows:
        for cell in row["places"].values():
            counts[cell["status"]] += 1
            if "UNRESOLVED" in str(cell.get("previous_status", "")):
                old_unresolved_resolutions[cell["status"]] += 1
    survivors = {
        side: [
            row["d"] for row in rows
            if row["side"] == side and all(cell["status"] == "YES" for cell in row["places"].values())
        ]
        for side in nxt.SIDES
    }
    return {
        "rows": len(rows),
        "places_per_row": 8,
        "cells": sum(counts.values()),
        "status_counts": counts,
        "previous_56_unresolved_resolved_as": old_unresolved_resolutions,
        "every_cell_resolved": counts["UNRESOLVED"] == 0,
        "surviving_ambient_classes": survivors,
        "warning": (
            "These are local ambient classes for the two isogeny descents, not computed Selmer groups. "
            "Only E-side d=35 is identified here as the rational component of the C_H 2-cover class."
        ),
    }


def build_certificate() -> dict[str, object]:
    rows = complete_local_matrix()
    torsor = torsor_projection_certificate()
    initial = nxt.matrix_summary()
    return {
        "schema": "PAPER_ELLIPTIC_CAMPBELL-local-matrix-v1",
        "source_sha256": {
            SCRIPT_PATH.name: sha256(SCRIPT_PATH),
            NEXT_PATH.name: sha256(NEXT_PATH),
        },
        "equations": {
            side: {"a": data["a"], "b": data["b"], "support": data["support"]}
            for side, data in nxt.SIDES.items()
        },
        "checked_places": ["infinity"] + [str(p) for p in nxt.BAD_PRIMES],
        "original_modulus_depths": {str(p): exponent for p, exponent in nxt.MODULUS_DEPTHS.items()},
        "initial_stage_survivors_16_plus_4": initial["survivors_after_proven_obstructions"],
        "initial_stage_unresolved_cells": initial["finite_cells_unresolved"],
        "torsor_projection": torsor,
        "summary": matrix_summary(rows),
        "rows": rows,
        "claim_boundary": {
            "proved": [
                "all 512 real/bad-prime cells in this 64-row ambient matrix are YES or NO",
                "the former 56 unresolved cells split as 24 YES at p=3 and 32 NO at p=59 or 71699",
                "the rational 2-torsion component of the C_H binary-quartic 2-cover class is E-side d=35",
            ],
            "not_proved": [
                "either ambient survivor set is a Selmer group",
                "C_H has or has no rational point",
                "the full H^1(Q,J_H[2]) class is determined by the single rational component d=35",
            ],
        },
    }


def main() -> None:
    certificate = build_certificate()
    CERTIFICATE_PATH.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(certificate["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
