"""Local, exact audit computations for the Campbell ninth-point fibre product.

Nothing in this file uses Magma or a remote service.  The bounded search is
complete for reduced m=a/b with b>0 and max(|a|,b) <= the requested bound.
Its negative output is deliberately labelled bounded evidence, not a proof
that the genus-one curve has no rational point.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import sympy as sp


M = sp.symbols("m")
D_COEFFS = (-264815, -19343520, 62846856064, -2906312951808, -495507443511296)
H_COEFFS = (-850079, -11210976, 138714149248, -5501355374592, -1679721044504576)
D_POLY = sp.Poly.from_list(D_COEFFS, gens=M)
H_POLY = sp.Poly.from_list(H_COEFFS, gens=M)


@dataclass(frozen=True)
class OddLocalCertificate:
    p: int
    m: int
    d_value: int
    d_root: int
    h_value: int
    h_root: int


# The same-m certificates from Round 02.  The generated JSON is the source
# hashed and checked by the Round 03 PowerShell/Magma audit wrapper.
ODD_LOCAL_CERTIFICATES = (
    OddLocalCertificate(3, 0, 1, 1, 1, 1),
    OddLocalCertificate(5, 0, 4, 2, 4, 2),
    OddLocalCertificate(7, 0, 1, 1, 4, 2),
    OddLocalCertificate(11, 0, 4, 2, 4, 2),
    OddLocalCertificate(13, 3, 3, 4, 1, 1),
    OddLocalCertificate(17, 0, 16, 4, 16, 4),
    OddLocalCertificate(19, 3, 11, 7, 11, 7),
    OddLocalCertificate(23, 1, 16, 4, 9, 3),
    OddLocalCertificate(29, 5, 28, 12, 25, 5),
    OddLocalCertificate(31, 1, 18, 7, 14, 13),
    OddLocalCertificate(37, 1, 1, 1, 25, 5),
    OddLocalCertificate(41, 2, 18, 10, 1, 1),
    OddLocalCertificate(43, 3, 1, 1, 35, 11),
    OddLocalCertificate(47, 6, 37, 15, 27, 11),
    OddLocalCertificate(53, 1, 10, 13, 1, 1),
    OddLocalCertificate(59, 12, 3, 11, 35, 25),
    OddLocalCertificate(61, 4, 36, 6, 46, 30),
    OddLocalCertificate(67, 3, 35, 13, 56, 18),
    OddLocalCertificate(71, 17, 58, 22, 38, 31),
    OddLocalCertificate(73, 0, 9, 3, 37, 16),
    OddLocalCertificate(79, 8, 2, 9, 19, 16),
    OddLocalCertificate(83, 2, 7, 16, 25, 5),
    OddLocalCertificate(89, 1, 55, 12, 34, 37),
    OddLocalCertificate(97, 1, 65, 29, 93, 44),
    OddLocalCertificate(8599, 5, 4872, 521, 3474, 1968),
    OddLocalCertificate(71699, 1, 13080, 12817, 43856, 30327),
    OddLocalCertificate(898543, 12, 593875, 198084, 686233, 420590),
    OddLocalCertificate(23037169, 1, 7173562, 1999717, 70894, 4416133),
    OddLocalCertificate(339106321, 1, 59232546, 46825223, 41459015, 138493612),
    OddLocalCertificate(1153266911, 0, 604401320, 115415469, 678697814, 139525893),
)

BRANCH_MODEL_BAD_PRIMES = (
    2, 3, 5, 7, 17, 19, 31, 59, 8599, 71699, 898543, 23037169,
    339106321, 1153266911,
)


def evaluate(coefficients: tuple[int, ...], value: int, modulus: int | None = None) -> int:
    result = 0
    for coefficient in coefficients:
        result = result * value + coefficient
        if modulus is not None:
            result %= modulus
    return result


def homogeneous_quartic(coefficients: tuple[int, ...], a: int, b: int) -> int:
    c4, c3, c2, c1, c0 = coefficients
    return c4*a**4 + c3*a**3*b + c2*a*a*b*b + c1*a*b**3 + c0*b**4


def is_square(value: int) -> bool:
    if value < 0:
        return False
    root = math.isqrt(value)
    return root * root == value


def binary_quartic_invariants(coefficients: tuple[int, ...]) -> tuple[int, int]:
    a, b, c, d, e = coefficients
    invariant_i = 12*a*e - 3*b*d + c*c
    invariant_j = 72*a*c*e + 9*b*c*d - 27*a*d*d - 27*b*b*e - 2*c**3
    return invariant_i, invariant_j


def quartic_and_jacobian_audit(coefficients: tuple[int, ...], scaling_u: int) -> dict[str, object]:
    poly = sp.Poly.from_list(coefficients, gens=M)
    disc = int(sp.discriminant(poly.as_expr(), M))
    invariant_i, invariant_j = binary_quartic_invariants(coefficients)
    invariant_disc = (4*invariant_i**3 - invariant_j**2) // 27
    assert 27*disc == 4*invariant_i**3 - invariant_j**2
    long_a = -27*invariant_i
    long_b = -27*invariant_j
    assert long_a % scaling_u**4 == 0
    assert long_b % scaling_u**6 == 0
    small_a = long_a // scaling_u**4
    small_b = long_b // scaling_u**6
    long_weierstrass_disc = -16*(4*long_a**3 + 27*long_b**2)
    small_weierstrass_disc = -16*(4*small_a**3 + 27*small_b**2)
    assert long_weierstrass_disc == 16*27**4*disc
    assert long_weierstrass_disc == scaling_u**12*small_weierstrass_disc
    return {
        "I": invariant_i,
        "J": invariant_j,
        "quartic_discriminant": disc,
        "invariant_discriminant": invariant_disc,
        "long_jacobian_model": [0, 0, 0, long_a, long_b],
        "integral_scaled_model": [0, 0, 0, small_a, small_b],
        "scaling_u": scaling_u,
        "long_weierstrass_discriminant": long_weierstrass_disc,
        "scaled_weierstrass_discriminant": small_weierstrass_disc,
        "minimality_claimed": False,
    }


def verify_odd_local_certificate(row: OddLocalCertificate) -> bool:
    d = evaluate(D_COEFFS, row.m, row.p)
    h = evaluate(H_COEFFS, row.m, row.p)
    return (
        d == row.d_value % row.p
        and h == row.h_value % row.p
        and row.d_root % row.p != 0
        and row.h_root % row.p != 0
        and row.d_root**2 % row.p == d
        and row.h_root**2 % row.p == h
    )


def root_isolation_certificate() -> list[dict[str, int]]:
    intervals = sp.intervals(H_POLY, eps=sp.Rational(1, 1000))
    assert len(intervals) == 4 and all(multiplicity == 1 for _, multiplicity in intervals)
    coarse = ((-416, -415), (-94, -93), (143, 144), (352, 353))
    result = []
    for ((left, right), multiplicity), (coarse_left, coarse_right) in zip(intervals, coarse):
        assert coarse_left < left < right < coarse_right
        result.append({
            "left_numerator": int(sp.numer(left)),
            "left_denominator": int(sp.denom(left)),
            "right_numerator": int(sp.numer(right)),
            "right_denominator": int(sp.denom(right)),
            "multiplicity": multiplicity,
        })
    assert all(evaluate(H_COEFFS, endpoint) < 0 for endpoint in (-416, -93, 143, 353))
    return result


def candidate_numerators(denominator: int, bound: int):
    # Exact root isolation proves H(a/b)>0 only inside these two wider
    # rational intervals.  They may include extra negative-H candidates but
    # never omit a square value.
    for lower, upper in ((-416, -93), (143, 353)):
        start = max(-bound, lower*denominator + 1)
        stop = min(bound, upper*denominator - 1)
        if start <= stop:
            yield from range(start, stop + 1)


def modular_tables(primes: tuple[int, ...]) -> dict[int, tuple[tuple[bool, ...], ...]]:
    tables = {}
    for p in primes:
        squares = {x*x % p for x in range(p)}
        table = []
        for b in range(p):
            table.append(tuple(homogeneous_quartic(H_COEFFS, a, b) % p in squares for a in range(p)))
        tables[p] = tuple(table)
    return tables


def search_ch_height(bound: int, sieve_primes: tuple[int, ...] = (11, 13, 17, 19, 23)) -> dict[str, object]:
    """Complete exact search for reduced m=a/b of naive projective height <= bound."""
    tables = modular_tables(sieve_primes)
    candidate_pairs = 0
    reduced_pairs = 0
    modular_survivors = 0
    ch_points: list[dict[str, int | bool]] = []
    for b in range(1, bound + 1):
        for a in candidate_numerators(b, bound):
            candidate_pairs += 1
            if math.gcd(abs(a), b) != 1:
                continue
            reduced_pairs += 1
            if any(not tables[p][b % p][a % p] for p in sieve_primes):
                continue
            modular_survivors += 1
            h_value = homogeneous_quartic(H_COEFFS, a, b)
            if not is_square(h_value):
                continue
            h_root = math.isqrt(h_value)
            d_value = homogeneous_quartic(D_COEFFS, a, b)
            ch_points.append({
                "a": a,
                "b": b,
                "H_homogeneous": h_value,
                "H_square_root": h_root,
                "D_homogeneous": d_value,
                "also_on_full_fibre_product": is_square(d_value),
                "D_square_root": math.isqrt(d_value) if is_square(d_value) else -1,
            })
    return {
        "height_definition": "b>0, gcd(|a|,b)=1, max(|a|,b)<=B",
        "bound_B": bound,
        "sieve_primes": list(sieve_primes),
        "candidate_pairs_in_proved_H_positive_superset": candidate_pairs,
        "reduced_pairs": reduced_pairs,
        "modular_survivors": modular_survivors,
        "CH_points": ch_points,
        "CH_point_count": len(ch_points),
        "full_fibre_product_point_count": sum(bool(point["also_on_full_fibre_product"]) for point in ch_points),
        "logical_status": "bounded evidence only",
    }


def build_certificate(bound: int) -> dict[str, object]:
    assert all(verify_odd_local_certificate(row) for row in ODD_LOCAL_CERTIFICATES)
    real_m = -400
    two_m = 1
    real_d = evaluate(D_COEFFS, real_m)
    real_h = evaluate(H_COEFFS, real_m)
    two_d = evaluate(D_COEFFS, two_m)
    two_h = evaluate(H_COEFFS, two_m)
    assert real_d > 0 and real_h > 0
    assert two_d % 8 == 1 and two_h % 8 == 1
    return {
        "classification": {
            "proved": [
                "the smooth Campbell fibre product has points over R and every Q_p",
                "the two quartic invariants and displayed integral Jacobian models satisfy the exact invariant identities",
            ],
            "awaiting_magma": [
                "the fake 2-Selmer set returned by an unbounded TwoCoverDescent(CH)",
            ],
            "bounded_evidence": [
                f"the exact CH rational search with max(|a|,b)<={bound}",
            ],
        },
        "coefficients": {"D": list(D_COEFFS), "H": list(H_COEFFS)},
        "branch_model_bad_primes": list(BRANCH_MODEL_BAD_PRIMES),
        "same_m_local_certificates": {
            "real": {"m": real_m, "D_m": real_d, "H_m": real_h},
            "two_adic": {"m": two_m, "D_m": two_d, "H_m": two_h, "D_mod_8": two_d % 8, "H_mod_8": two_h % 8},
            "odd_format": ["p", "m", "D_mod_p", "sqrt_D", "H_mod_p", "sqrt_H"],
            "odd": [[row.p, row.m, row.d_value, row.d_root, row.h_value, row.h_root] for row in ODD_LOCAL_CERTIFICATES],
            "remaining_good_primes": "p>=101 outside branch-model bad set; genus-5 Weil lower bound is positive, then smooth points Hensel lift",
        },
        "root_isolation_for_search": root_isolation_certificate(),
        "binary_quartic_audits": {
            "D": quartic_and_jacobian_audit(D_COEFFS, 32),
            "H": quartic_and_jacobian_audit(H_COEFFS, 64),
        },
        "bounded_CH_search": search_ch_height(bound),
        "global_status": {
            "CH_rational_point_known": False,
            "full_fibre_product_rational_point_known": False,
            "fake_two_selmer_computed": False,
        },
    }


def canonical_json_bytes(certificate: dict[str, object]) -> bytes:
    return (json.dumps(certificate, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=50000)
    parser.add_argument("--output", default=str(Path(__file__).resolve().parent.parent / "certificates" / "same_m_local.json"))
    args = parser.parse_args()
    certificate = build_certificate(args.bound)
    payload = canonical_json_bytes(certificate)
    Path(args.output).write_bytes(payload)
    print("certificate_sha256", hashlib.sha256(payload).hexdigest())
    print(json.dumps(certificate["bounded_CH_search"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
