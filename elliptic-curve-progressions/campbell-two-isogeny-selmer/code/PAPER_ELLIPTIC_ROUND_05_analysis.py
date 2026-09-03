"""Exact arithmetic for the remaining d=35 Cassels--Tate input.

This file deliberately uses only Python integers (and SymPy for the initial
square roots modulo odd primes).  It does not claim that the tangent-line
formula has been proved in this repository; it provides the auditable local
arithmetic to which that standard theorem would be applied.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from sympy.ntheory.residue_ntheory import sqrt_mod

import PAPER_ELLIPTIC_ROUND_04_analysis as round04


A = -591_895_071
B = 58_536_289_153_843_200
D = 1_434_501_462_453_361
d = 35
C = B // d
e = 4_230_241
e_other = 339_106_321

ROOT = Path(__file__).resolve().parent
CERTIFICATE_PATH = ROOT / "PAPER_ELLIPTIC_ROUND_05_CERTIFICATE.json"

# A rational point on Q_d: N^2=d R^2+A R S+C S^2.
CONIC_POINT = (16_257_024, 1, 36_058_176)

# Primitive tangent at CONIC_POINT.  It is retained only as an audited
# candidate local function: the old report did not define a legitimate
# Cassels--Tate pairing to which it could be applied.
TANGENT = (60_677_401, -697_502_396_215_296, -8_012_928)

LOCAL_UV = {
    2: (1, 1),
    3: (9, 1),
    5: (1, 1),
    7: (1, 1),
    59: (0, 1),
    71_699: (0, 1),
    339_106_321: (0, 1),
}


def quartic_rhs(U: int, V: int) -> int:
    return d * U**4 + A * U**2 * V**2 + C * V**4


def conic_value(R: int, S: int, N: int) -> int:
    return d * R * R + A * R * S + C * S * S - N * N


def tangent_value(R: int, S: int, N: int) -> int:
    lr, ls, ln = TANGENT
    return lr * R + ls * S + ln * N


def vp(n: int, p: int) -> int:
    if n == 0:
        raise ValueError("v_p(0) is not finite")
    n = abs(n)
    ans = 0
    while n % p == 0:
        ans += 1
        n //= p
    return ans


def _unit_square_roots_mod_prime_power(unit: int, p: int, exponent: int) -> list[int]:
    """All roots needed here of x^2=unit mod p^exponent."""
    if exponent <= 0:
        return [0]
    modulus = p**exponent
    unit %= modulus
    if p == 2:
        if exponent <= 3:
            return [x for x in range(modulus) if x * x % modulus == unit]
        roots = [x for x in range(8) if x * x % 8 == unit % 8]
        current = 8
        while current < modulus:
            roots = sorted(
                {
                    y
                    for x in roots
                    for y in (x, x + current)
                    if y * y % (2 * current) == unit % (2 * current)
                }
            )
            current *= 2
        return roots

    roots_p = [int(x) for x in sqrt_mod(unit % p, p, all_roots=True)]
    roots: list[int] = []
    for root in roots_p:
        mod = p
        while mod < modulus:
            # root -> root+t*mod and divide the congruence by mod modulo p.
            error = (unit - root * root) // mod
            t = (error * pow(2 * root, -1, p)) % p
            root += t * mod
            mod *= p
        roots.append(root % modulus)
    return sorted(set(roots))


def square_roots_padic_mod(rhs: int, p: int, precision: int) -> list[int]:
    valuation = vp(rhs, p)
    if valuation % 2:
        return []
    half = valuation // 2
    if precision <= half:
        raise ValueError("precision must exceed half the valuation")
    unit = rhs // p**valuation
    unit_exponent = precision - half
    roots = _unit_square_roots_mod_prime_power(unit, p, unit_exponent)
    modulus = p**precision
    # Adding multiples of p^(precision-half) before multiplying by p^half
    # gives the same residue modulo p^precision.
    return sorted({(p**half * r) % modulus for r in roots})


def legendre_unit(unit: int, p: int) -> int:
    residue = pow(unit % p, (p - 1) // 2, p)
    if residue == 1:
        return 1
    if residue == p - 1:
        return -1
    raise ValueError("argument is not a p-adic unit")


def hilbert_symbol(A0: int, B0: int, p: int) -> int:
    """Hilbert symbol (A0,B0)_p for nonzero integer representatives."""
    alpha, beta = vp(A0, p), vp(B0, p)
    u, v = A0 // p**alpha, B0 // p**beta
    if p == 2:
        u %= 8
        v %= 8
        exponent = (
            ((u - 1) // 2) * ((v - 1) // 2)
            + alpha * ((v * v - 1) // 8)
            + beta * ((u * u - 1) // 8)
        ) % 2
        return -1 if exponent else 1
    exponent = (alpha * beta * ((p - 1) // 2)) % 2
    ans = -1 if exponent else 1
    if beta % 2:
        ans *= legendre_unit(u, p)
    if alpha % 2:
        ans *= legendre_unit(v, p)
    return ans


def local_tangent_data(p: int, pairing_class: int, precision: int = 12) -> list[dict]:
    U, V = LOCAL_UV[p]
    rhs = quartic_rhs(U, V)
    # Increase precision if the tangent value vanishes to the requested order.
    while True:
        modulus = p**precision
        roots = square_roots_padic_mod(rhs, p, precision)
        rows = []
        unresolved = False
        for N in roots:
            Lres = tangent_value(U * U, V * V, N) % modulus
            if Lres == 0:
                unresolved = True
                break
            lv = vp(Lres, p)
            # Lres agrees with the actual p-adic value through p^precision,
            # hence its valuation and unit mod p are certified when lv<precision.
            rows.append(
                {
                    "N_mod": N,
                    "modulus": modulus,
                    "quartic_residual_mod": (N * N - rhs) % modulus,
                    "L_mod": Lres,
                    "L_valuation": lv,
                    "L_unit_mod_p": (Lres // p**lv) % p,
                    "hilbert_symbol": hilbert_symbol(Lres, pairing_class, p),
                }
            )
        if not unresolved:
            return rows
        precision *= 2
        if precision > 64:
            raise RuntimeError("tangent value remained unresolved")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate_payload() -> dict:
    R0, S0, N0 = CONIC_POINT
    conic = {
        "equation": "N^2=35*R^2-591895071*R*S+1672465404395520*S^2",
        "global_point": {"R": R0, "S": S0, "N": N0},
        "point_residual": conic_value(R0, S0, N0),
        "primitive_tangent_coefficients_R_S_N": list(TANGENT),
        "tangent_at_global_point": tangent_value(R0, S0, N0),
        "quartic_pullback": "L_35=60677401*U^2-697502396215296*V^2-8012928*N",
    }
    # Reproduce the formerly proposed evaluation with e=59*71699.  This is
    # an audit of a rejected formula, not a Cassels--Tate computation.
    local = {}
    for p in LOCAL_UV:
        precision = 20 if p == 2 else (3 if p in (59, 71_699) else 5)
        local[str(p)] = {
            "U": LOCAL_UV[p][0],
            "V": LOCAL_UV[p][1],
            "rhs": quartic_rhs(*LOCAL_UV[p]),
            "precision_exponent": precision,
            "branches": local_tangent_data(p, e, precision),
        }

    symbols_59 = [row["hilbert_symbol"] for row in local["59"]["branches"]]
    symbols_71699 = [row["hilbert_symbol"] for row in local["71699"]["branches"]]
    products = sorted(
        set(x * y for x, y in itertools.product(symbols_59, symbols_71699))
    )
    assert symbols_59 == [-1, 1]
    assert symbols_71699 == [-1, 1]
    assert products == [-1, 1]

    selmer = round04.isogeny_selmer_certificate()["exact_selmer_groups"]
    matrix_path = ROOT / "PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json"
    round04_path = ROOT / "PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json"
    same_m_path = ROOT / "STUDENT_ELLIPTIC_ROUND_03_certificate.json"
    magma_path = ROOT / "PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m"
    return {
        "schema": "paper-elliptic-campbell-round-05-correction-v1",
        "claim_boundary": {
            "proved": [
                "the auxiliary conic has the displayed rational point and primitive tangent",
                "the formerly proposed local expression has branch-dependent values at 59 and 71699",
                "the two exact isogeny Selmer groups and rank upper bound from Round 04 remain valid",
            ],
            "withdrawn": [
                "that <35,4230241> is a defined Cassels--Tate pairing between opposite isogeny Selmer groups",
                "that the displayed tangent line computes such a pairing",
                "that one opposite-side bit can prove C_H(Q) is empty",
            ],
            "not_proved": [
                "the full 2-Selmer group or a basis of full 2-coverings",
                "any Cassels--Tate pairing involving the class of C_H",
                "C_H(Q) is empty or nonempty",
            ],
        },
        "exact_isogeny_selmer_groups_reused": selmer,
        "conic_and_tangent": conic,
        "rejected_opposite_side_formula_audit": {
            "proposed_second_argument": e,
            "proposed_second_argument_factorization": "4230241=59*71699",
            "warning": (
                "These Hilbert symbols are not promoted to Cassels--Tate values. "
                "The arguments 35 and 4230241 live in opposite isogeny Selmer groups, "
                "whereas the standard isogeny Cassels--Tate pairing used to test lifting "
                "is defined on one Sel^(dual phi) group squared."
            ),
            "local_data": local,
            "branch_symbols": {"59": symbols_59, "71699": symbols_71699},
            "possible_products_from_independent_local_branches": products,
            "well_definedness_test": "FAIL_BRANCH_INDEPENDENCE",
        },
        "required_next_objects": {
            "same_side_isogeny_pairing": (
                "To test the image Sel^2(E/Q)->Sel^(dual phi)(E'/Q), construct the "
                "pairing on Sel^(dual phi)(E'/Q) x itself; 35 must be paired with "
                "same-side classes, not with 4230241."
            ),
            "full_two_selmer_pairing": (
                "To test the Campbell class itself, compute a basis of Sel^2(E/Q) as "
                "everywhere locally soluble binary quartics with the same invariants, "
                "identify z(H) in the cubic etale algebra Q x K, and pair H with those "
                "full 2-coverings using an explicit full-2-Selmer formula."
            ),
        },
        "source_sha256": {
            "PAPER_ELLIPTIC_ROUND_05_analysis.py": sha256(Path(__file__)),
            "PAPER_ELLIPTIC_CAMPBELL_CERTIFICATE.json": sha256(matrix_path),
            "PAPER_ELLIPTIC_ROUND_04_CERTIFICATE.json": sha256(round04_path),
            "STUDENT_ELLIPTIC_ROUND_03_certificate.json": sha256(same_m_path),
            "PAPER_ELLIPTIC_ROUND_05_full_two_selmer.m": sha256(magma_path),
        },
    }


if __name__ == "__main__":
    payload = certificate_payload()
    CERTIFICATE_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["rejected_opposite_side_formula_audit"]["branch_symbols"], sort_keys=True))
