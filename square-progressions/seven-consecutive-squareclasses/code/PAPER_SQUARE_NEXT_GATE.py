"""Exact fourth-round gate for the remaining 54 squareclass patterns.

The selection score is purely finite.  The mask-102 integral-point theorem is
proved by a gcd/squarefree argument; bounded search is not used.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path


MASK77_CERT = Path("PAPER_SQUARE_MASK77_CERTIFICATE.json")
ROUND4_CERT = Path("STUDENT_SQUARE_ROUND_04_CERTIFICATE.json")
OUTPUT = Path("PAPER_SQUARE_NEXT_GATE_CERTIFICATE.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def support(mask: int) -> list[int]:
    return [i for i in range(7) if (mask >> i) & 1]


def constant_pairing(mask: int):
    roots = support(mask)
    if len(roots) != 4:
        return None
    first = roots[0]
    for mate in roots[1:]:
        left = (first, mate)
        right = tuple(x for x in roots if x not in left)
        if sum(left) == sum(right):
            constant = right[0] * right[1] - left[0] * left[1]
            return {"left": list(left), "right": list(right), "difference_right_minus_left": constant}
    return None


def squarefree_divisors(n: int) -> list[int]:
    primes = []
    value = n
    p = 2
    while p*p <= value:
        if value % p == 0:
            primes.append(p)
            while value % p == 0:
                value //= p
        p += 1
    if value > 1:
        primes.append(value)
    answers = [1]
    for p in primes:
        answers += [p*d for d in answers]
    return sorted(answers)


def remaining_rows():
    mask77 = json.loads(MASK77_CERT.read_text(encoding="utf-8"))
    round4 = json.loads(ROUND4_CERT.read_text(encoding="utf-8"))
    remaining = set(mask77["same_t_pattern_audit"]["remaining_pattern_ids"])
    rows = [row for row in round4["pattern_occurrences"] if row["pattern_id"] in remaining]
    assert len(rows) == len(remaining) == 54
    for row in rows:
        masks = [item["character_mask_m"] for item in row["occurrences"]]
        assert len(masks) == len(set(masks)) == 15
    return rows


def ranking():
    rows = remaining_rows()
    frequency = Counter(
        item["character_mask_m"]
        for row in rows for item in row["occurrences"]
        if item["genus"] == 1
    )
    candidates = []
    for mask, count in frequency.items():
        pairing = constant_pairing(mask)
        if pairing is None:
            continue
        bound = abs(pairing["difference_right_minus_left"])
        candidates.append({
            "mask": mask,
            "support": support(mask),
            "patterns_hit": count,
            "constant_pairing": pairing,
            "gcd_bound": bound,
            "squarefree_kernel_candidates_upper_bound": squarefree_divisors(bound),
        })
    # Primary score: number of remaining patterns hit; secondary score: smaller
    # constant/gcd support.  The full divisor analysis is done for the winner.
    return sorted(candidates, key=lambda row: (-row["patterns_hit"], row["gcd_bound"], row["mask"]))


def mask102_rhs(t: int) -> int:
    return (t+1)*(t+2)*(t+5)*(t+6)


def mask102_integral_point_certificate():
    """Complete proof data for y^2=(t+1)(t+2)(t+5)(t+6)."""
    middle = []
    for t in range(-6, 0):
        value = mask102_rhs(t)
        square = value >= 0 and math.isqrt(value) ** 2 == value
        middle.append({"t": t, "rhs": value, "is_square": square})
    assert [row["t"] for row in middle if row["is_square"]] == [-6, -5, -2, -1]

    # Outside [-6,-1], A and B are positive.  Since B-A=4 and AB is a
    # square, their common positive squarefree kernel divides 4, hence d=1,2.
    d1_factor_pairs = [(r, 4 // r) for r in (1, 2, 4) if 4 % r == 0]
    d1_same_parity = [pair for pair in d1_factor_pairs if (pair[0]-pair[1]) % 2 == 0]
    assert d1_same_parity == [(2, 2)]
    # (V-U,V+U)=(2,2) forces U=0, hence A=0: only a branch point.
    squares_mod4 = {x*x % 4 for x in range(4)}
    differences_mod4 = {(v-u) % 4 for u in squares_mod4 for v in squares_mod4}
    assert 2 not in differences_mod4
    return {
        "curve": "y^2=(t+1)(t+2)(t+5)(t+6)",
        "A": "(t+1)(t+6)",
        "B": "(t+2)(t+5)",
        "B_minus_A": 4,
        "positive_regions": ["t<=-7", "t>=0"],
        "middle_interval_exact_check": middle,
        "common_positive_squarefree_kernels": [1, 2],
        "d=1": {
            "equation": "V^2-U^2=4",
            "factor_pairs_of_4": [list(pair) for pair in d1_factor_pairs],
            "same_parity_pairs": [list(pair) for pair in d1_same_parity],
            "consequence": "U=0,V=2, so A=0 (branch only)",
        },
        "d=2": {
            "equation": "V^2-U^2=2",
            "squares_mod_4": sorted(squares_mod4),
            "square_differences_mod_4": sorted(differences_mod4),
            "consequence": "impossible modulo 4",
        },
        "proved_integral_points": [[-6,0],[-5,0],[-2,0],[-1,0]],
        "nondegenerate_integral_points": [],
        "status": "PROVED_COMPLETE_BY_GCD_AND_FINITE_MIDDLE_INTERVAL",
    }


def pattern_impact():
    rows = remaining_rows()
    affected = sorted(row["pattern_id"] for row in rows if any(
        item["character_mask_m"] == 102 for item in row["occurrences"]
    ))
    assert len(affected) == 19
    old = sorted(row["pattern_id"] for row in rows)
    survivors = sorted(set(old) - set(affected))
    assert len(survivors) == 35
    return {
        "input_remaining_count": 54,
        "selected_mask": 102,
        "affected_pattern_ids": affected,
        "strictly_excluded": 19,
        "remaining_count": 35,
        "remaining_pattern_ids": survivors,
        "reason": "mask 102 has no nondegenerate integral parameter, so no same-t candidate exists",
    }


def build_certificate():
    ranks = ranking()
    assert ranks[0]["mask"] == 102 and ranks[0]["patterns_hit"] == 19
    return {
        "schema": "paper-square-next-gate-v1",
        "input_sha256": {
            MASK77_CERT.name: sha256(MASK77_CERT),
            ROUND4_CERT.name: sha256(ROUND4_CERT),
        },
        "selection_rule": "maximize remaining patterns hit among four-root masks with a constant quadratic pairing; break ties by smaller gcd bound",
        "constant_pairing_ranking": ranks,
        "mask102_integral_points": mask102_integral_point_certificate(),
        "pattern_impact": pattern_impact(),
    }


def main():
    OUTPUT.write_text(json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
