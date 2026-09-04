"""Uniform two- and three-adic gate for the Campbell E-prime covers.

This module uses only the Python standard library.  The proof implemented
here is symbolic: the old 512-cell matrix is read only to verify that its
rows agree with the uniform congruence criteria.  No modular enumeration is
used to prove the theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
OUTPUT = PROJECT / "certificates" / "round10_eprime_two_three_gate.json"
LOCAL_MATRIX = PROJECT / "certificates" / "local_matrix_512.json"

A = 1_183_790_142
C = A // 2
B = 116_194_618_458_722_241
D = B // 3**4
DELTA = A * A - 4 * B
K2 = DELTA // 2**22
SUPPORT = (3, 59, 71_699, 339_106_321)

EXPECTED_Q2 = (
    1,
    177,
    215_097,
    4_230_241,
    339_106_321,
    60_021_818_817,
    72_940_752_328_137,
    1_434_501_462_453_361,
)
EXPECTED_Q3 = (
    -24_313_584_109_379,
    -20_007_272_939,
    -71_699,
    -59,
    1,
    4_230_241,
    339_106_321,
    1_434_501_462_453_361,
)
EXPECTED_INTERSECTION = (1, 4_230_241, 339_106_321, 1_434_501_462_453_361)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valuation(value: int, prime: int) -> int:
    assert value
    answer = 0
    while value % prime == 0:
        value //= prime
        answer += 1
    return answer


def signed_squarefree_candidates() -> tuple[int, ...]:
    positive = []
    for length in range(len(SUPPORT) + 1):
        positive.extend(
            _product(choice) for choice in itertools.combinations(SUPPORT, length)
        )
    return tuple(sorted([-d for d in positive] + positive))


def _product(values: tuple[int, ...]) -> int:
    answer = 1
    for value in values:
        answer *= value
    return answer


def q2_soluble(d: int) -> bool:
    """The proved Q_2 criterion for supported squarefree d."""
    assert d in signed_squarefree_candidates()
    return d % 8 == 1


def q3_soluble(d: int) -> bool:
    """The proved Q_3 criterion for supported squarefree d."""
    assert d in signed_squarefree_candidates()
    return valuation(d, 3) == 0 and d % 3 == 1


def local_matrix_audit() -> dict[str, object]:
    """Check that the uniform theorem recovers the old E-prime cells."""
    matrix = json.loads(LOCAL_MATRIX.read_text(encoding="utf-8"))
    rows = [row for row in matrix["rows"] if row["side"] == "E_dual"]
    assert len(rows) == 32
    assert tuple(row["d"] for row in rows) == signed_squarefree_candidates()

    disagreements: list[dict[str, object]] = []
    for row in rows:
        d = int(row["d"])
        for prime, predicted in (("2", q2_soluble(d)), ("3", q3_soluble(d))):
            stored = row["places"][prime]["status"] == "YES"
            if stored != predicted:
                disagreements.append(
                    {"d": d, "prime": int(prime), "stored": stored, "proved": predicted}
                )
    assert not disagreements

    finite_places = ["2", "3", "5", "7", "59", "71699", "339106321"]
    target = list(EXPECTED_INTERSECTION)
    minimal_pairs = []
    for left, right in itertools.combinations(finite_places, 2):
        survivors = [
            row["d"]
            for row in rows
            if row["places"][left]["status"] == "YES"
            and row["places"][right]["status"] == "YES"
        ]
        if survivors == target:
            minimal_pairs.append([int(left), int(right)])
    one_place_sizes = {
        prime: sum(row["places"][prime]["status"] == "YES" for row in rows)
        for prime in finite_places
    }
    assert min(one_place_sizes.values()) == 8
    assert minimal_pairs == [[2, 3], [2, 5]]
    return {
        "source_path": "certificates/local_matrix_512.json",
        "source_sha256": sha256(LOCAL_MATRIX),
        "eprime_rows": len(rows),
        "checked_cells": 64,
        "disagreements": disagreements,
        "one_place_survivor_counts": one_place_sizes,
        "minimum_number_of_finite_places_for_four_stored_survivors": 2,
        "all_minimal_pairs_with_the_same_four_stored_survivors": minimal_pairs,
        "chosen_uniform_pair": [2, 3],
        "choice_reason": (
            "Both places admit short valuation proofs; the alternative pair (2,5) "
            "is recorded but is not needed for the theorem."
        ),
    }


def proof_certificate() -> dict[str, object]:
    candidates = signed_squarefree_candidates()
    q2 = tuple(d for d in candidates if q2_soluble(d))
    q3 = tuple(d for d in candidates if q3_soluble(d))
    both = tuple(d for d in candidates if q2_soluble(d) and q3_soluble(d))
    assert q2 == EXPECTED_Q2
    assert q3 == EXPECTED_Q3
    assert both == EXPECTED_INTERSECTION
    assert A == 2 * C
    assert B == 3**4 * 59 * 71_699 * 339_106_321
    assert DELTA == 2**22 * K2
    assert K2 % 2 == 1
    assert C % 8 == 7 and B % 8 == 1
    assert valuation(A, 3) == 2
    assert (A // 9) % 3 == 1 and D % 3 == 1

    return {
        "curve": {
            "equation": "E': y^2=x^3+A*x^2+B*x",
            "A": A,
            "B": B,
            "A_over_2": C,
            "B_over_3_to_the_4": D,
            "A_squared_minus_4B": DELTA,
            "A_squared_minus_4B_over_2_to_the_22": K2,
        },
        "cover": "C'_d: N^2=d*U^4+A*U^2*V^2+(B/d)*V^4",
        "support": list(SUPPORT),
        "all_32_candidates": list(candidates),
        "two_adic": {
            "criterion": "C'_d(Q_2) is nonempty iff d=1 mod 8",
            "survivors": list(q2),
            "identity": (
                "d*N^2=T^2-2^20*K*V^4, where T=d*U^2+(A/2)*V^2 "
                "and K=(A^2-4B)/2^22 is odd"
            ),
            "necessity": {
                "primitive_opposite_parity": "T is odd",
                "primitive_both_odd": (
                    "if d is 3, 5, or 7 mod 8 then v_2(T) is respectively 1, 2, or 1"
                ),
                "square_unit_step": (
                    "the correction has valuation at least 20-2*v_2(T)>=16; "
                    "1+2^16 Z_2 consists of squares, forcing d to be a Q_2-square"
                ),
            },
            "sufficiency_hensel": {
                "polynomial": "f(X)=X^2-d",
                "approximate_root": 1,
                "condition": "v_2(f(1))>=3>2*v_2(f'(1))=2",
                "cover_point": "(U:V:N)=(1:0:sqrt(d))",
            },
        },
        "three_adic": {
            "criterion": "C'_d(Q_3) is nonempty iff v_3(d)=0 and d=1 mod 3",
            "survivors": list(q3),
            "necessity": {
                "v3_d_equals_1": (
                    "for a primitive pair the unique least term has valuation 1 if U is a unit "
                    "and valuation 3 if 3 divides U"
                ),
                "v3_d_equals_0_U_unit": "F_d=d*U^4 mod 3",
                "v3_d_equals_0_v3U_at_least_2": "F_d/3^4=(D/d)*V^4 mod 3",
                "v3_d_equals_0_v3U_equals_1": (
                    "F_d/3^4=d*u^4+(A/9)*u^2*V^2+(D/d)*V^4; "
                    "for d=-1 mod 3 its residue is -1+1-1=-1"
                ),
            },
            "sufficiency_hensel": {
                "polynomial": "f(X)=X^2-d",
                "approximate_root": 1,
                "condition": "f(1)=0 mod 3 and f'(1)=2 is a 3-adic unit",
                "cover_point": "(U:V:N)=(1:0:sqrt(d))",
            },
        },
        "intersection": {
            "survivors": list(both),
            "factor_description": ["1", "59*71699", "339106321", "59*71699*339106321"],
        },
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "campbell-eprime-two-three-gate-v1",
        "source_sha256": {Path(__file__).name: sha256(Path(__file__))},
        "theorem": proof_certificate(),
        "matrix_compatibility_audit": local_matrix_audit(),
        "claim_boundary": {
            "proved": [
                "the exact Q_2 classification of all 32 supported E-prime cover classes",
                "the exact Q_3 classification of all 32 supported E-prime cover classes",
                "their intersection is exactly the four displayed classes",
                "two finite places are minimal for recovering these four rows from the stored matrix",
            ],
            "not_proved": [
                "a rational ninth point or a global obstruction on the Campbell curve",
                "an independent second-CAS reproduction",
                "priority or novelty from a finite literature search",
            ],
        },
    }


def main() -> None:
    OUTPUT.write_text(
        json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
